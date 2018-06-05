from yg.emanate.events import Event


class TestEvent(object):

    def test_event_type(self):
        assert Event.event_type is None
