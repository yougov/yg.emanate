"""Classes for observers in ``emanate``."""
import logging
from threading import Thread

from six.moves import queue
from pika.exceptions import AMQPError, RecursionError
from pikachewie.data import Properties
from pikachewie.helpers import broker_from_config
from pikachewie.publisher import BlockingJSONPublisher

__metaclass__ = type

log = logging.getLogger(__name__)


class BasePublisher:
    """Base Publisher class."""
    def __init__(self, *args, **kwargs):
        pass

    def publish(self, event):
        pass


NullPublisher = BasePublisher
"""Publisher that silently discards all events."""


class QueuePublisher(BasePublisher):
    """Publisher that dispatches events to a `queue.Queue`."""
    def __init__(self):
        self._queue = queue.Queue(maxsize=256)
        self._worker = Thread(target=self._process_queue)
        self._worker.daemon = True
        self._worker.start()

    def publish(self, event):
        try:
            self._queue.put_nowait(event)
        except queue.Full as exc:
            log.exception('Cannot publish event: %r', exc)
            log.warn('Failed to publish event %s with context %s',
                     event.data, event.context)

    def _process_queue(self):
        while True:
            event = self._queue.get()
            try:
                self._process_event(event)
            except Exception as exc:
                log.exception(exc)
            finally:
                self._queue.task_done()

    def _process_event(self, event):
        pass


class RabbitMQPublisher(QueuePublisher):
    """Publisher that publishes events as messages to RabbitMQ.

    By default, messages are published on a headers exchange. The name of the
    exchange is given in the `config` passed to the Publisher's constructor.

    """
    def __init__(self, config, broker_name='default'):
        self.config = config
        self.broker_name = broker_name
        self.broker = broker_from_config(
            self.config['rabbitmq']['brokers'][self.broker_name]
        )
        self.publisher = BlockingJSONPublisher(self.broker)
        self.exchange = self.config['rabbitmq']['default_exchange']
        self._initialize()
        super(RabbitMQPublisher, self).__init__()

    def _initialize(self):
        # declare the exchange (will trigger a connection to the broker)
        self.publisher.channel.exchange_declare(
            self.exchange,
            **self.config['rabbitmq']['exchanges'][self.exchange]
        )

    def _wait_for_event(self):
        while True:
            # trigger processing of RabbitMQ data events
            try:
                self.publisher.process_data_events()
            except Exception as exc:
                log.exception('Error processing data events: %r', exc)
                del self.publisher.channel

            try:
                return self._queue.get(timeout=10)
            except queue.Empty:
                pass

    def _process_queue(self):
        while True:
            event = self._wait_for_event()
            self._handle_event(event)

    def _handle_event(self, event):
        try:
            self._process_event(event)
        except Exception as exc:
            log.exception(exc)
        finally:
            self._queue.task_done()

    def _process_event(self, event):
        properties = Properties()
        if event.context:
            properties.headers = event.context
        routing_key = properties.headers.get('routing_key', '')

        try:
            self.publisher.publish(self.exchange, routing_key, event.data, properties)
        except (AMQPError, RecursionError) as exc:
            log.exception('Cannot publish to RabbitMQ: %r', exc)
            log.warn('Failed to publish message payload %s with context %s',
                     event.data, event.context)
