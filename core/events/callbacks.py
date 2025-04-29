"""
Module core/events/callbacks.py

Provides callback handlers for game events such as stat modifications and theme toggles.
These functions are designed to be registered with the EventManager to update game state
and adjust UI in response to user actions or system events.
"""

import logging
from themes.theme_manager import set_theme, get_theme_name

logger = logging.getLogger(__name__)


def modify_stat(stat_manager, stat_name: str, amount: float) -> None:
    """
    Adjust the specified statistic by a given amount.

    Args:
        stat_manager: The StatManager instance containing game statistics.
        stat_name (str): The key of the statistic to modify.
        amount (float): The delta to apply to the stat value.

    Logs a warning if the statistic key is not found.
    """
    if stat_name in getattr(stat_manager, 'stats', {}):
        stat_manager.modify(stat_name, amount)
        logger.debug("Modified stat '%s' by %s", stat_name, amount)
    else:
        logger.warning("Stat '%s' not found. Cannot modify.", stat_name)


def toggle_theme() -> None:
    """
    Toggle the application UI theme between 'light' and 'dark'.

    If current theme is 'light' or 'retro', switches to 'dark'; otherwise
    switches back to 'light'. Logs the theme transition.
    """
    current = get_theme_name()
    new = "dark" if current in ("light", "retro") else "light"
    logger.info("Toggling theme from %s to %s.", current, new)
    set_theme(new)


def set_retro() -> None:
    """
    Set the UI theme to 'retro' style.

    Logs the change and forces the 'retro' theme.
    """
    current = get_theme_name()
    logger.info("Toggling theme from %s to 'retro'.", current)
    set_theme("retro")
