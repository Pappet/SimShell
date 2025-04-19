import pytest
import pygame
import sys
import setup.config as config

# Configure known values for tests
config.SCREEN_WIDTH = 800
config.SCREEN_HEIGHT = 600
config.TITLE = "TestGame"
config.FONT_SIZE = 16
config.FONT_NAME = "TestFont"

# Dummy implementations for pygame/display and other dependencies
class DummyScreen:
    def __init__(self):
        self.fill_color = None
        self.blits = []
    def fill(self, color):
        self.fill_color = color
    def blit(self, surface, pos):
        self.blits.append((surface, pos))

class DummyDisplay:
    def __init__(self):
        self.caption = None
        self.flipped = False
    def set_mode(self, size):
        self.mode = size
        return DummyScreen()
    def set_caption(self, title):
        self.caption = title
    def flip(self):
        self.flipped = True

class DummyClock:
    def __init__(self):
        self.ticked = []
    def tick(self, fps):
        self.ticked.append(fps)

class DummyFont:
    pass  # No-op; DebugConsole uses render but we test run flow only

class DummyEvent:
    def __init__(self, type):
        self.type = type

class DummyContext:
    def __init__(self, debug_console):
        self.debug_console_passed = debug_console

class DummySceneManager:
    def __init__(self, context, debug_console):
        self.context = context
        self.debug_console = debug_console
        self.switch_scene_called = []
        self.last_event = None
        self.updated = False
        self.drawn_surface = None
    def switch_scene(self, key):
        self.switch_scene_called.append(key)
    def handle_event(self, event):
        self.last_event = event
    def update(self):
        self.updated = True
    def draw(self, surface):
        self.drawn_surface = surface

@pytest.fixture(autouse=True)
def dummy_environment(monkeypatch):
    # Dummy display
    dummy_display = DummyDisplay()
    monkeypatch.setattr(pygame.display, 'set_mode', lambda size: dummy_display.set_mode(size))
    monkeypatch.setattr(pygame.display, 'set_caption', lambda title: dummy_display.set_caption(title))
    monkeypatch.setattr(pygame.display, 'flip', lambda : dummy_display.flip())
    # Dummy clock
    monkeypatch.setattr(pygame.time, 'Clock', lambda: DummyClock())
    # Dummy font
    monkeypatch.setattr(pygame.font, 'SysFont', lambda name, size: DummyFont())
    # Quit and exit
    monkeypatch.setattr(pygame, 'quit', lambda: setattr(dummy_display, 'quit_called', True))
    monkeypatch.setattr(sys, 'exit', lambda: (_ for _ in ()).throw(SystemExit))
    # Monkeypatch core.app dependencies
    import core.app
    monkeypatch.setattr(core.app, 'GameContext', DummyContext)
    monkeypatch.setattr(core.app, 'SceneManager', DummySceneManager)
    return dummy_display


def test_init_sets_up_components(dummy_environment):
    from core.app import GameApp
    from core.debug_console import DebugConsole

    app = GameApp()
    # Screen and display
    assert hasattr(dummy_environment, 'mode')
    assert dummy_environment.caption == "TestGame"
    # Clock
    assert isinstance(app.clock, DummyClock)
    # Font and debug_console
    assert isinstance(app.font, DummyFont)
    assert hasattr(app.debug_console, 'draw')
    # Context and scene_manager
    assert isinstance(app.context, DummyContext)
    assert app.context.debug_console_passed is app.debug_console
    assert isinstance(app.scene_manager, DummySceneManager)
    # switch_scene called with 'menu'
    assert app.scene_manager.switch_scene_called == ["menu"]
    # Running flag
    assert app.running is True


def test_run_loop_breaks_on_quit(dummy_environment, monkeypatch):
    # Prepare event sequence: first no events, then a QUIT
    sequence = [[], [pygame.QUIT]]
    monkeypatch.setattr(pygame.event, 'get', lambda: [DummyEvent(t) for t in sequence.pop(0)])

    from core.app import GameApp
    app = GameApp()
    # Run should exit via SystemExit
    with pytest.raises(SystemExit):
        app.run()
    # Ensure tick was called
    assert 60 in app.clock.ticked
    # Ensure pygame.quit was called
    assert getattr(dummy_environment, 'quit_called', False) is True
