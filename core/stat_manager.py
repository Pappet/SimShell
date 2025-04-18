# core/stat_manager.py
import json
from core.events.event_types import EventType
from core.decorators import ensure_key
from collections import namedtuple

'''
StatManager class for managing game statistics.
It provides methods to get, set, and modify statistics like energy.
It also integrates with an event manager to dispatch events when statistics change.
'''

# 1. Metadaten‑Definition für jede Stat
StatConfig = namedtuple("StatConfig", ["initial", "min", "max", "event_type"])

class StatManager:
    def __init__(self, event_manager, debug_console, config_path="setup/stats_config.json"):
        self.debug_console = debug_console
        self.event_manager = event_manager

        # 1) JSON‑Datei einlesen
        try:
            with open(config_path, "r") as f:
                raw = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.debug_console.log(f"Error loading stats config: {e}")
            raw = {}

        # 2) Aus rohen Daten StatConfig‐Mappings erzeugen
        self._stat_configs = {}
        for key, cfg in raw.items():
            # EventType aus String holen, Standard: None
            ev = None
            try:
                ev = EventType[cfg["event_type"]]
            except KeyError:
                self.debug_console.log(f"Unknown event_type '{cfg['event_type']}' for stat '{key}'")
            self._stat_configs[key] = StatConfig(
                initial=cfg.get("initial", 0),
                min=cfg.get("min", 0),
                max=cfg.get("max", cfg.get("initial", 0)),
                event_type=ev
            )

        # 3) stats‐ und event_map‐Dicts automatisch erzeugen
        self.stats     = {k: c.initial for k, c in self._stat_configs.items()}
        # 4) event_map: stat_name -> event_type
        self._event_map = {k: c.event_type for k, c in self._stat_configs.items()}

        self.debug_console.log(f"Initial stats: {self.stats}")
        self.debug_console.log("StatManager initialized with event map.")

    @ensure_key
    def get(self, key):
        self.debug_console.log(f"Getting stat '{key}': {self.stats[key]}")
        return self.stats.get(key, 0)
    
    @ensure_key
    def get_max(self, key):
        self.debug_console.log(f"Getting max from stat '{key}': {self._stat_configs[key].max}")
        return self._stat_configs[key].max
    
    @ensure_key
    def get_min(self, key):
        self.debug_console.log(f"Getting min from stat '{key}': {self._stat_configs[key].min}")
        return self._stat_configs[key].min

    @ensure_key    
    def set(self, key, value):
        cfg = self._stat_configs[key]
        old_value = self.stats[key]

        # 2. Clamp auf min/max
        new_value = max(cfg.min, min(cfg.max, value))

        # 3. Wenn kein Unterschied, abbrechen
        if new_value == old_value:
            self.debug_console.log(
                f"Stat '{key}' remains unchanged at {old_value} (clamped between {cfg.min}–{cfg.max})."
            )
            return False

        # 4. Andernfalls updaten und dispatchen
        self.stats[key] = new_value
        self.debug_console.log(f"Setting stat '{key}' to {new_value}")
        event = self._event_map.get(key)
        if event:
            self.event_manager.dispatch(event, new_value=new_value)

        return True

    @ensure_key
    def modify(self, key, delta):        
        self.debug_console.log(
            f"Modifying stat '{key}' by {delta}. Current value: {self.stats[key]}"
        )
        # set() loggt und dispatcht – und gibt True/False zurück
        return self.set(key, self.get(key) + delta)