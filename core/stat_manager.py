"""
Module core/stat_manager.py

Provides StatManager for loading, tracking, and updating game statistics.
Loads stat configurations from JSON, clamps values within defined ranges,
and dispatches events via the EventManager on stat changes.
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

# Data structure to hold configuration for each stat: initial value, min, max, and event type
StatConfig = namedtuple("StatConfig", ["initial", "min", "max", "event_type"])


class StatManager:
    """
    Manages game statistics with support for clamping and event-driven updates.

    Attributes:
        event_manager (EventManager): Dispatcher for stat change events.
        stats (Dict[str, float]): Current values of all managed statistics.
    """
    def __init__(
        self,
        event_manager: Any,
        config_path: str = None
    ) -> None:
        """
        Initialize the StatManager and load stat definitions.

        Args:
            event_manager (Any): EventManager to dispatch change events.
            config_path (str, optional): Filepath to JSON stat config. Defaults to
                Config.paths['stats_config'].
        """
        self.event_manager = event_manager
        # Determine config file path, use default if not provided
        self.config_path = config_path or Config.paths["stats_config"]

        # Load and parse stat configuration JSON
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                raw: Dict[str, Any] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(
                f"Error loading stats config from {self.config_path}: {e}",
                exc_info=True
            )
            raw = {}

        # Build internal mapping from stat key to StatConfig
        self._stat_configs: Dict[str, StatConfig] = {}
        for key, cfg in raw.items():
            # Determine associated event type, if configured
            ev_type = None
            try:
                ev_type = EventType[cfg.get("event_type")]
            except Exception:
                logger.error(
                    f"Unknown event_type '{cfg.get('event_type')}' for stat '{key}'",
                    exc_info=True
                )
            # Store config with defaults for missing fields
            self._stat_configs[key] = StatConfig(
                initial=cfg.get("initial", 0),
                min=cfg.get("min", 0),
                max=cfg.get("max", cfg.get("initial", 0)),
                event_type=ev_type
            )

        # Initialize current stat values based on initial config
        self.stats: Dict[str, float] = {
            k: sc.initial for k, sc in self._stat_configs.items()
        }
        # Map stat keys to event types for dispatching
        self._event_map: Dict[str, EventType] = {
            k: sc.event_type for k, sc in self._stat_configs.items()
        }

        logger.debug(f"StatManager initialized with stats: {self.stats}")

    @ensure_key
    def get(self, key: str) -> float:
        """
        Retrieve the current value of a statistic.

        Args:
            key (str): The stat identifier.

        Returns:
            float: Current value (or 0 if not set).
        """
        value = self.stats.get(key, 0)
        logger.debug(f"Getting stat '{key}': {value}")
        return value

    @ensure_key
    def get_max(self, key: str) -> float:
        """
        Retrieve the maximum allowed value for a statistic.

        Args:
            key (str): The stat identifier.

        Returns:
            float: Configured maximum value.
        """
        max_value = self._stat_configs[key].max
        logger.debug(f"Getting max for stat '{key}': {max_value}")
        return max_value

    @ensure_key
    def get_min(self, key: str) -> float:
        """
        Retrieve the minimum allowed value for a statistic.

        Args:
            key (str): The stat identifier.

        Returns:
            float: Configured minimum value.
        """
        min_value = self._stat_configs[key].min
        logger.debug(f"Getting min for stat '{key}': {min_value}")
        return min_value

    @ensure_key
    def set(self, key: str, value: float) -> bool:
        """
        Set a new value for a statistic, clamped between its min and max.
        Dispatches an event if the value changes.

        Args:
            key (str): The stat identifier.
            value (float): New desired value.

        Returns:
            bool: True if the value was changed, False if unchanged.
        """
        cfg = self._stat_configs[key]
        old_value = self.stats[key]
        # Clamp value within allowed range
        new_value = max(cfg.min, min(cfg.max, value))
        if new_value == old_value:
            logger.debug(
                f"Stat '{key}' unchanged at {old_value} (clamped {cfg.min}-{cfg.max})."
            )
            return False

        # Update and dispatch event
        self.stats[key] = new_value
        logger.debug(f"Stat '{key}' set to {new_value}")
        event_type = self._event_map.get(key)
        if event_type:
            self.event_manager.dispatch(event_type, new_value=new_value)
        return True

    @ensure_key
    def modify(self, key: str, delta: float) -> bool:
        """
        Change a statistic by a delta amount, respecting min/max limits.
        Dispatches an event if the value changes.

        Args:
            key (str): The stat identifier.
            delta (float): Amount to adjust the stat by.

        Returns:
            bool: True if the value was changed.
        """
        logger.debug(f"Modifying stat '{key}' by {delta}")
        # Use set() to handle clamping and event dispatch
        return self.set(key, self.get(key) + delta)
