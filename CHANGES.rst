0.6.0
-----

* ``RabbitMQPublisher`` will look for a `routing_key` context parameter on
  an event, and will use that value as the routing key for the event.

0.5.0
-----

* Drop support for Python 2.6 and 3.3.

0.4.0
-----

* Rename package to yg.emanate.

0.3.0
-----

* If ``RabbitMQPublisher`` encounters an AMQP error while processing data
  events, attempt to re-establish the underlying channel (#1 from
  @the-allanc).
* Make ``RabbitMQPublisher`` more robust in its handling of errors that
  occur while processing data events. (#3 from @the-allanc).

0.2.1
-----

* Bump to PikaChewie>=1.1.1.

0.2.0
-----

* Python 3 compatibility.

0.1.0
-----

* Initial release.
