"""
Module core/context.py

Defines the GameContext class, which centralizes game-wide services and state:
- EventManager for broadcasting events
- StatManager for tracking and updating game statistics
- SoundManager for loading and playing audio
- Reference to PluginManager for plugin-driven extensions
"""

import logging

from core.stat_manager import StatManager
from core.events.event_manager import EventManager
from core.plugin_manager import PluginManager
from core.sound_manager import SoundManager

logger = logging.getLogger(__name__)


class GameContext:
    """
    Container for game-wide managers and shared state.

    This class provides a central access point for key subsystems used
    throughout the game, including event dispatching, stat tracking,
    sound playback, and plugin coordination.
    """
    def __init__(self, plugin_manager: PluginManager):
        """
        Initialize core subsystems and dependencies for gameplay.

        Args:
            plugin_manager (PluginManager): The plugin manager instance
                to allow context-aware plugin interactions.
        """
        # Core event dispatcher for decoupled message passing
        self.event_manager = EventManager()

        # Statistic manager: loads stat config and dispatches change events
        self.stat_manager = StatManager(event_manager=self.event_manager)

        # Sound system: handles loading and playing sound effects/music
        self.sound_manager = SoundManager()

        # Keep a reference to the plugin manager for extension hooks
        self.plugin_manager = plugin_manager

        logger.debug("GameContext initialized.")
