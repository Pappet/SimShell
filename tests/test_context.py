import pytest
from core.context import GameContext

# Dummy implementations for testing
class DummyConsole:
    def __init__(self):
        self.logs = []
    def log(self, msg):
        self.logs.append(msg)

class DummyEventManager:
    def __init__(self, debug_console):
        self.debug_console = debug_console

class DummyStatManager:
    def __init__(self, event_manager, debug_console):
        self.event_manager = event_manager
        self.debug_console = debug_console

@pytest.fixture(autouse=True)
def patch_managers(monkeypatch):
    # Patch EventManager and StatManager in core.context
    import core.context as ctx_mod
    monkeypatch.setattr(ctx_mod, 'EventManager', DummyEventManager)
    monkeypatch.setattr(ctx_mod, 'StatManager', DummyStatManager)

@pytest.fixture
def dummy_console():
    return DummyConsole()

def test_game_context_initialization(dummy_console):
    ctx = GameContext(debug_console=dummy_console)
    # Ensure event_manager and stat_manager are our dummy classes
    assert isinstance(ctx.event_manager, DummyEventManager)
    assert ctx.event_manager.debug_console is dummy_console
    assert isinstance(ctx.stat_manager, DummyStatManager)
    assert ctx.stat_manager.event_manager is ctx.event_manager
    assert ctx.stat_manager.debug_console is dummy_console
    # Check that GameContext initialization was logged
    assert "GameContext initialized." in dummy_console.logs
