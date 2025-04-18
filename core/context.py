# core/context.py

'''
GameContext class for managing the game context.
It serves as a central point for managing game resources and states.
It includes an event manager and a stat manager.
'''

from core.stat_manager import StatManager
from core.events.event_manager import EventManager
import logging

logger = logging.getLogger(__name__)

class GameContext:
    def __init__(self, debug_console):        
        self.event_manager = EventManager(debug_console=debug_console)
        self.stat_manager = StatManager(event_manager=self.event_manager, debug_console=debug_console)
        self.debug_console = debug_console
        logger.debug("GameContext initialized.")