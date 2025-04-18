import pytest
import json
from core.stat_manager import StatManager
from core.events.event_types import EventType

class DummyConsole:
    def __init__(self):
        self.logs = []
    def log(self, msg):
        self.logs.append(msg)

class DummyEventManager:
    def __init__(self):
        self.dispatched = []
    def dispatch(self, event_type, *args, **kwargs):
        self.dispatched.append((event_type, args, kwargs))

@pytest.fixture
def write_config(tmp_path):
    # Create a temporary JSON config file
    config = {
        "energy": {"initial": 100, "min": 0, "max": 150, "event_type": "ENERGY_CHANGED"},
        "health": {"initial": 50, "min": 0, "max": 100, "event_type": "HEALTH_CHANGED"}
    }
    file_path = tmp_path / "stats_config.json"
    with open(file_path, "w") as f:
        json.dump(config, f)
    return str(file_path)

@pytest.fixture
def console():
    return DummyConsole()

@pytest.fixture
def event_manager():
    return DummyEventManager()

@pytest.fixture
def manager(event_manager, console, write_config):
    # Pass the path to the JSON config
    return StatManager(event_manager, console, config_path=write_config)


def test_init_loads_and_logs(console, event_manager, write_config):
    console.logs.clear()
    StatManager(event_manager, console, config_path=write_config)
    # Initialization log first
    assert "StatManager initialized." in console.logs
    # After init, stats attribute should match config initial values
    sm = StatManager(event_manager, console, config_path=write_config)
    assert sm.stats == {"energy": 100, "health": 50}


def test_get_existing_stats(manager, console):
    console.logs.clear()
    assert manager.get("energy") == 100
    assert "Getting stat 'energy': 100" in console.logs


def test_get_missing_stat_returns_zero_and_logs(manager, console):
    console.logs.clear()
    assert manager.get("unknown") == 0
    # Decorator logs missing key with 'Cannot get.'
    assert console.logs == ["Stat 'unknown' not found. Cannot get."]


def test_set_within_bounds_updates_and_dispatches(manager, console, event_manager):
    console.logs.clear()
    result = manager.set("health", 80)
    assert result is True
    assert manager.stats["health"] == 80
    assert console.logs[-1] == "Setting stat 'health' to 80"
    assert (EventType.HEALTH_CHANGED, (), {"new_value": 80}) in event_manager.dispatched


def test_set_above_max_clamps_and_logs(manager, console, event_manager):
    console.logs.clear()
    result = manager.set("energy", 200)
    assert result is True
    assert manager.stats["energy"] == 150  # max clamp
    assert "Setting stat 'energy' to 150" in console.logs
    assert (EventType.ENERGY_CHANGED, (), {"new_value": 150}) in event_manager.dispatched


def test_set_below_min_clamps_and_logs(manager, console, event_manager):
    console.logs.clear()
    result = manager.set("energy", -10)
    assert result is True
    assert manager.stats["energy"] == 0
    assert "Setting stat 'energy' to 0" in console.logs
    assert (EventType.ENERGY_CHANGED, (), {"new_value": 0}) in event_manager.dispatched


def test_set_no_change_returns_false_and_logs(manager, console, event_manager):
    console.logs.clear()
    # energy initial is 100, setting to 100 yields no change
    result = manager.set("energy", 100)
    assert result is False
    # Should log that value remains unchanged
    assert any("Stat 'energy' remains unchanged at 100" in msg for msg in console.logs)
    assert event_manager.dispatched == []
    assert event_manager.dispatched == []


def test_set_unknown_key_returns_false_and_logs(manager, console, event_manager):
    console.logs.clear()
    result = manager.set("unknown", 10)
    assert result is False
    assert console.logs == ["Stat 'unknown' not found. Cannot set."]
    assert event_manager.dispatched == []


def test_modify_changes_value_and_dispatches(manager, console, event_manager):
    console.logs.clear()
    result = manager.modify("energy", -20)
    assert result is True
    assert manager.stats["energy"] == 80
    # Logs include modifying and setting
    assert any("Modifying stat 'energy' by -20" in msg for msg in console.logs)
    assert any("Setting stat 'energy' to 80" in msg for msg in console.logs)
    assert (EventType.ENERGY_CHANGED, (), {"new_value": 80}) in event_manager.dispatched


def test_modify_no_effect_returns_false_and_logs(manager, console):
    console.logs.clear()
    # health initial 50, modify by 0 yields no change
    result = manager.modify("health", 0)
    assert result is False
    # Should log that value remains unchanged
    assert any("Stat 'health' remains unchanged at 50" in msg for msg in console.logs)


def test_modify_unknown_key_returns_false_and_logs(manager, console, event_manager):
    console.logs.clear()
    result = manager.modify("unknown", 5)
    assert result is False
    assert console.logs == ["Stat 'unknown' not found. Cannot modify."]
    assert event_manager.dispatched == []
