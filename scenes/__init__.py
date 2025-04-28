"""
Module core/event_types.py

Defines EventType enum representing various game event categories.
Used by EventManager and listeners to identify event semantics.
"""

from .main_menu_scene import MainMenuScene
from .game_scene import GameScene
from .plugin_manager_scene import PluginManagerScene
from enum import Enum, auto


class EventType(Enum):
    """
    Enumeration of event types dispatched throughout the game.

    Attributes:
        UI_BUTTON_CLICKED: Triggered when any UI button is clicked.
        ENERGY_CHANGED: Dispatched when the ENERGY stat value is modified.
        HEALTH_CHANGED: Dispatched when the HEALTH stat value is modified.
    """
    UI_BUTTON_CLICKED = auto()
    ENERGY_CHANGED = auto()
    HEALTH_CHANGED = auto()
