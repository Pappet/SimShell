import pytest
from core.scene_manager import SceneManager
from core.scene_registry import scene_registry


class DummyConsole:
    def __init__(self):
        self.logs = []

    def log(self, msg):
        self.logs.append(msg)


class DummyScene:
    def __init__(self, context, switch_callback):
        self.context = context
        self.switch_callback = switch_callback
        self.handled_events = []
        self.updated = False
        self.drawn_on = None

    def handle_event(self, event):
        self.handled_events.append(event)

    def update(self):
        self.updated = True

    def draw(self, surface):
        self.drawn_on = surface


@pytest.fixture(autouse=True)
def clear_registry():
    # Ensure registry is empty before each test
    scene_registry.clear()


@pytest.fixture
def dummy_context():
    return {'foo': 'bar'}


@pytest.fixture
def dummy_console():
    return DummyConsole()


@pytest.fixture
def manager(dummy_context, dummy_console):
    return SceneManager(dummy_context, dummy_console)


def test_switch_to_and_current_scene(manager):
    scene = DummyScene(manager.context, manager.switch_scene)
    manager.switch_to(scene)
    assert manager.current_scene is scene


def test_switch_scene_creates_and_caches(manager, dummy_context, dummy_console):
    # Register DummyScene under key 'key'
    scene_registry['key'] = DummyScene

    manager.switch_scene('key')
    # A new scene should have been created and set as current
    assert isinstance(manager.current_scene, DummyScene)
    first_instance = manager.current_scene
    # The scene should have received the correct context and callback
    assert first_instance.context is dummy_context
    # Bound methods create new wrapper objects each access, so compare underlying function and instance
    assert hasattr(first_instance.switch_callback, "__self__") and first_instance.switch_callback.__self__ is manager
    assert first_instance.switch_callback.__func__ is SceneManager.switch_scene

    # Switching again should use the cached instance (not create a new one)
    manager.switch_scene('key')
    assert manager.current_scene is first_instance


def test_switch_scene_invalid_key_logs(manager, dummy_console):
    manager.switch_scene('invalid')
    assert "Scene for key: 'invalid' not found." in dummy_console.logs


def test_handle_event_delegation(manager):
    scene = DummyScene(manager.context, manager.switch_scene)
    manager.switch_to(scene)
    event = object()
    manager.handle_event(event)
    assert scene.handled_events == [event]


def test_handle_event_no_scene(manager):
    # Should not raise even if no scene is set
    manager.handle_event(object())


def test_update_delegation(manager):
    scene = DummyScene(manager.context, manager.switch_scene)
    manager.switch_to(scene)
    manager.update()
    assert scene.updated is True


def test_update_no_scene(manager):
    manager.update()  # Should not raise


def test_draw_delegation(manager):
    scene = DummyScene(manager.context, manager.switch_scene)
    manager.switch_to(scene)
    surface = object()
    manager.draw(surface)
    assert scene.drawn_on is surface


def test_draw_no_scene(manager):
    manager.draw(object())  # Should not raise


def test_debug_console_switch_logs(manager, dummy_console):
    scene_registry['k'] = DummyScene
    manager.switch_scene('k')
    # Ensure that switching logs the action
    assert any("Switching to scene:" in log for log in dummy_console.logs)
