import pytest
import sys
from core.events import callbacks

class DummyStatManager:
    def __init__(self):
        self.calls = []
    def modify(self, stat, amount):
        self.calls.append((stat, amount))


def test_add_energy_calls_modify():
    sm = DummyStatManager()
    callbacks.add_energy(sm)
    assert sm.calls == [("energy", 10)]


def test_subtract_energy_calls_modify():
    sm = DummyStatManager()
    callbacks.subtract_energy(sm)
    assert sm.calls == [("energy", -10)]


def test_start_game_prints_message(capsys):
    callbacks.start_game()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Game started!"
    assert captured.err == ""


def test_exit_game_prints_and_exits(capsys):
    with pytest.raises(SystemExit):
        callbacks.exit_game()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Exiting game..."
    assert captured.err == ""
