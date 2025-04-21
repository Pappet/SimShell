# core/event_types.py
from enum import Enum, auto

class EventType(Enum):
    """
    Enum for different types of events in the game.
    """
    ENERGY_CHANGED = auto()
    HEALTH_CHANGED = auto()