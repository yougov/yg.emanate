"""Classes for events in ``emanate``."""
import blinker
from jaraco.classes.properties import classproperty

__metaclass__ = type


class Event:
    """Base class for ``emanate`` events."""
    event_type = None

    def __init__(self, extra_context=None, extra_data=None):
        self._context = extra_context if extra_context else {}
        self._data = extra_data if extra_data else {}

    @property
    def context(self):
        context = {
            'event_type': self.event_type,
        }
        context.update(self._context)
        return context

    @property
    def data(self):
        data = self.context
        data.update(self._data)
        return data

    @classproperty
    def _signal(cls):
        return blinker.signal(cls.event_type)

    @classmethod
    def register_observer(cls, observer):
        if not callable(observer):
            raise ValueError('observer must be callable')
        cls._signal.connect(observer)

    @classmethod
    def unregister_observer(cls, observer):
        if not callable(observer):
            raise ValueError('observer must be callable')
        cls._signal.disconnect(observer)

    def emit(self):
        self._signal.send(self)
