# core/context.py

'''
GameContext class for managing the game context.
It serves as a central point for managing game resources and states.
It includes an event manager and a stat manager.
'''

from core.stat_manager import StatManager
from core.events.event_manager import EventManager
from core.plugin_manager import PluginManager
import logging

logger = logging.getLogger(__name__)

class GameContext:
    def __init__(self, plugin_manager):        
        self.event_manager = EventManager()
        self.stat_manager = StatManager(event_manager=self.event_manager)
        self.plugin_manager = plugin_manager
        logger.debug("GameContext initialized.")