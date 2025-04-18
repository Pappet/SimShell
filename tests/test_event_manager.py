import pytest
from core.events.event_types import EventType
from core.events.event_manager import EventManager

class DummyConsole:
    def __init__(self):
        self.logs = []
    def log(self, msg):
        self.logs.append(msg)

@pytest.fixture
def console():
    return DummyConsole()

@pytest.fixture
def manager(console):
    return EventManager(console)

class DummyEventType:
    TEST = "TEST_EVENT"


def test_register_logs_and_stores_listener(manager, console):
    def callback(): pass

    manager.register(DummyEventType.TEST, callback)
    # Listener stored
    assert DummyEventType.TEST in manager.listeners
    assert manager.listeners[DummyEventType.TEST] == [callback]
    # Log entry
    assert console.logs == [f"Registering callback for event: {DummyEventType.TEST}"]


def test_unregister_logs_and_removes_listener(manager, console):
    def callback(): pass
    # Pre-populate listener
    manager.listeners.setdefault(DummyEventType.TEST, []).append(callback)

    manager.unregister(DummyEventType.TEST, callback)
    # Listener list should be empty
    assert manager.listeners[DummyEventType.TEST] == []
    # Log entry for unregister
    assert console.logs == [f"Unregistering callback for event: {DummyEventType.TEST}"]


def test_unregister_nonexistent_event_type_does_nothing(manager, console):
    # No listeners for this type
    manager.unregister(DummyEventType.TEST, lambda: None)
    # No logs should be produced
    assert console.logs == []


def test_dispatch_logs_and_invokes_callbacks(manager, console):
    results = []
    def cb1(arg, kw=None): results.append(("cb1", arg, kw))
    def cb2(arg, kw=None): results.append(("cb2", arg, kw))

    manager.register(DummyEventType.TEST, cb1)
    manager.register(DummyEventType.TEST, cb2)
    console.logs.clear()

    manager.dispatch(DummyEventType.TEST, 42, kw="value")

    # Dispatch logged
    assert console.logs == [f"Dispatching event: {DummyEventType.TEST} with args: (42,), kwargs: {{'kw': 'value'}}"]
    # Both callbacks invoked in order
    assert results == [("cb1", 42, "value"), ("cb2", 42, "value")]


def test_dispatch_with_response_logs_and_returns(manager, console):
    def cb1(): return 1
    def cb2(): return 2

    manager.register(DummyEventType.TEST, cb1)
    manager.register(DummyEventType.TEST, cb2)
    console.logs.clear()

    responses = manager.dispatch_with_response(DummyEventType.TEST)

    # Dispatch with response logged
    assert console.logs == [f"Dispatching event with response: {DummyEventType.TEST} with args: (), kwargs: {{}}"]
    # Responses collected
    assert responses == [1, 2]


def test_dispatch_no_listeners_still_logs(manager, console):
    console.logs.clear()
    manager.dispatch("NON_EXISTENT", 7)
    assert console.logs == ["Dispatching event: NON_EXISTENT with args: (7,), kwargs: {}"]


def test_dispatch_with_response_no_listeners_returns_empty(manager, console):
    console.logs.clear()
    responses = manager.dispatch_with_response("NONE")
    assert console.logs == ["Dispatching event with response: NONE with args: (), kwargs: {}"]
    assert responses == []
