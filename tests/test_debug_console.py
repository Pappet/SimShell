import pytest
import pygame
from core.debug_console import DebugConsole

# Dummy implementations for font and surfaces
class DummySurface:
    def __init__(self, text):
        self.text = text
    def get_height(self):
        return 10

class DummyFont:
    def render(self, text, antialias, color):
        # Return a DummySurface embedding the text for inspection
        return DummySurface(text)

class DummyCanvas:
    def __init__(self):
        self.blits = []
    def blit(self, surface, pos):
        self.blits.append((surface, pos))


def test_log_adds_timestamp(monkeypatch):
    # Simulate pygame.time.get_ticks() returning 3500 ms
    monkeypatch.setattr(pygame.time, 'get_ticks', lambda: 3500)
    font = DummyFont()
    console = DebugConsole(font, max_lines=5)
    console.log("hello")
    # 3500 ms => 3 seconds
    assert console.logs == ["3: hello"]


def test_log_eviction(monkeypatch):
    # Simulate time fixed at 1000 ms (= 1 s)
    monkeypatch.setattr(pygame.time, 'get_ticks', lambda: 1000)
    font = DummyFont()
    console = DebugConsole(font, max_lines=3)
    # Log five messages; only last 3 should be kept
    for i in range(5):
        console.log(f"msg{i}")
    expected = [f"1: msg{i}" for i in range(2, 5)]
    assert console.logs == expected


def test_clear_clears_logs():
    font = DummyFont()
    console = DebugConsole(font)
    console.logs = ["a", "b", "c"]
    console.clear()
    assert console.logs == []


def test_draw_blits_text_surfaces(monkeypatch):
    font = DummyFont()
    console = DebugConsole(font)
    # Pre-populate logs
    console.logs = ["first line", "second line"]
    canvas = DummyCanvas()
    # Draw at position (20, 30)
    console.draw(canvas, pos=(20, 30))
    # Internal offset subtracts 10: (10, 20)
    assert len(canvas.blits) == 2
    surf1, pos1 = canvas.blits[0]
    surf2, pos2 = canvas.blits[1]
    assert isinstance(surf1, DummySurface)
    assert surf1.text == "first line"
    assert pos1 == (10, 20)
    # Next y should be 20 + height(10) + 2 = 32
    assert isinstance(surf2, DummySurface)
    assert surf2.text == "second line"
    assert pos2 == (10, 32)
