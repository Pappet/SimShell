"""
Module core/events/callbacks.py

Provides callback handlers for game events such as stat modifications and theme toggles.
These functions are designed to be registered with the EventManager to update game state
and adjust UI in response to user actions or system events.
"""

import logging
from themes.theme_manager import set_theme, get_theme_name, THEMES

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
    Toggle the application UI theme durch alle verfügbaren Themes in THEMES.

    Ermittelt den aktuellen Theme-Namen, findet dessen Index in der
    THEMES-Liste und wechselt zum nächsten Eintrag (zyklisch).
    Logs die Theme-Transition.
    """
    # Liste aller Theme-Namen in der Reihenfolge der dict-Definition
    theme_names = list(THEMES.keys())
    current = get_theme_name()
    try:
        idx = theme_names.index(current)
    except ValueError:
        # Falls current nicht in THEMES ist, zurück auf erstes Theme
        idx = 0
        logger.warning("Unbekanntes Theme '%s', wechsle auf '%s'.", current, theme_names[idx])

    # Nächstes Theme, zyklisch
    new = theme_names[(idx + 1) % len(theme_names)]
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


def on_toggle(state):
    print(f"Checkbox is now: {state}")

def update_label_text(label, text):
    logger.info("Set Text: %s of Label: %s ", text, label)
    label.set_text(text)