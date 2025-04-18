'''
This module contains callback functions for the game. These functions are called when certain events occur in the game, 
such as starting or exiting the game, or modifying player stats.
They are designed to be used with the event manager and stat manager to handle game state changes and UI updates.
'''
import logging
from themes.theme_manager import set_theme, get_theme_name

logger = logging.getLogger(__name__)

def modify_stat(stat_manager, stat_name, amount):
    if stat_name in stat_manager.stats:
        stat_manager.modify(stat_name, amount)
    else:
        logger.warning(f"Stat '{stat_name}' not found. Cannot modify.")

def toggle_theme():
    current = get_theme_name()
    new = "dark" if current in ("light", "retro") else "light"
    logger.info(f"Toggling theme from {current} to {new}.")
    set_theme(new)

def toggle_retro():
    current = "retro"
    logger.info(f"Toggling theme to {current}.")
    set_theme(current)