# core/stat_manager.py

"""
StatManager handles game statistics: loading configuration, clamping values,
and dispatching change events through the event manager.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict
from collections import namedtuple

from core.events.event_types import EventType
from core.decorators import ensure_key
import setup.config as Config

logger = logging.getLogger(__name__)

# Named tuple to store stat configuration metadata
StatConfig = namedtuple("StatConfig", ["initial", "min", "max", "event_type"])

class StatManager:
    """
    Manages game statistics and integrates with an EventManager to dispatch
    events when stat values change.
    """
    def __init__(
        self,
        event_manager: Any,
        config_path: str = None
    ) -> None:
        """
        Initialize the StatManager and load stat configurations from JSON.

        Args:
            event_manager (Any): EventManager to dispatch stat change events.
            config_path (str, optional): Path to the stats config file.
                Defaults to Config.paths['stats_config'].
        """
        self.event_manager = event_manager
        # Use default path if none provided
        self.config_path = config_path or Config.paths["stats_config"]

        # Load raw JSON configuration
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                raw: Dict[str, Any] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Error loading stats config from {self.config_path}: {e}", exc_info=True)
            raw = {}

        # Build StatConfig mappings
        self._stat_configs: Dict[str, StatConfig] = {}
        for key, cfg in raw.items():
            ev_type = None
            try:
                ev_type = EventType[cfg.get("event_type")]
            except Exception:
                logger.error(
                    f"Unknown event_type '{cfg.get('event_type')}' for stat '{key}'", exc_info=True
                )
            self._stat_configs[key] = StatConfig(
                initial=cfg.get("initial", 0),
                min=cfg.get("min", 0),
                max=cfg.get("max", cfg.get("initial", 0)),
                event_type=ev_type
            )

        # Initialize stat values and event map
        self.stats: Dict[str, float] = {k: sc.initial for k, sc in self._stat_configs.items()}
        self._event_map: Dict[str, EventType] = {k: sc.event_type for k, sc in self._stat_configs.items()}

        logger.debug(f"StatManager initialized with stats: {self.stats}")

    @ensure_key
    def get(self, key: str) -> float:
        """
        Get the current value of a statistic.

        Args:
            key (str): Name of the statistic.

        Returns:
            float: Current stat value.
        """
        value = self.stats.get(key, 0)
        logger.debug(f"Getting stat '{key}': {value}")
        return value

    @ensure_key
    def get_max(self, key: str) -> float:
        """
        Get the maximum allowed value for a statistic.

        Args:
            key (str): Name of the statistic.

        Returns:
            float: Maximum stat value.
        """
        max_value = self._stat_configs[key].max
        logger.debug(f"Getting max for stat '{key}': {max_value}")
        return max_value

    @ensure_key
    def get_min(self, key: str) -> float:
        """
        Get the minimum allowed value for a statistic.

        Args:
            key (str): Name of the statistic.

        Returns:
            float: Minimum stat value.
        """
        min_value = self._stat_configs[key].min
        logger.debug(f"Getting min for stat '{key}': {min_value}")
        return min_value

    @ensure_key
    def set(self, key: str, value: float) -> bool:
        """
        Set a new value for a statistic, clamped between its min and max,
        and dispatch an event if the value changed.

        Args:
            key (str): Name of the statistic.
            value (float): New stat value.

        Returns:
            bool: True if the value changed, False otherwise.
        """
        cfg = self._stat_configs[key]
        old_value = self.stats[key]
        new_value = max(cfg.min, min(cfg.max, value))
        if new_value == old_value:
            logger.debug(
                f"Stat '{key}' unchanged at {old_value} (clamped {cfg.min}-{cfg.max})."
            )
            return False
        self.stats[key] = new_value
        logger.debug(f"Stat '{key}' set to {new_value}")
        event_type = self._event_map.get(key)
        if event_type:
            self.event_manager.dispatch(event_type, new_value=new_value)
        return True

    @ensure_key
    def modify(self, key: str, delta: float) -> bool:
        """
        Modify a statistic by a delta amount and dispatch change event.

        Args:
            key (str): Name of the statistic.
            delta (float): Amount to change the stat by.

        Returns:
            bool: True if the value changed, False otherwise.
        """
        logger.debug(f"Modifying stat '{key}' by {delta}")
        return self.set(key, self.get(key) + delta)
