"""
Module themes/theme_manager.py

Manages UI color themes: loading, switching, and retrieving theme colors.
Defines functions to set and query the active theme, as well as utility
for generating random colors.
"""

import random
from typing import Dict, Tuple, Any

from themes import dark_theme, light_theme, retro_theme, dracula_theme
import setup.config as Config

logger = __import__('logging').getLogger(__name__)

# Pre-defined theme mappings loaded from respective modules
THEMES: Dict[str, Dict[str, Tuple[int, ...]]] = {
    "dark": dark_theme.theme,
    "light": light_theme.theme,
    "retro": retro_theme.theme,
    "dracula": dracula_theme.theme
}

# Initialize active theme based on configuration default, fallback to dark
_current_theme_name: str = Config.theme.get("default", "dark")
_current_theme: Dict[str, Tuple[int, ...]] = THEMES.get(
    _current_theme_name,
    dark_theme.theme
)


def set_theme(name: str) -> None:
    """
    Switch the current UI theme to the specified theme name.

    Args:
        name (str): Key of the theme to activate ("dark", "light", or "retro").

    If the provided name is not found, the current theme remains unchanged.
    """
    global _current_theme, _current_theme_name
    if name in THEMES:
        _current_theme = THEMES[name]
        _current_theme_name = name
        logger.info("Theme switched to '%s'.", name)
    else:
        logger.warning(
            "Attempted to set unknown theme '%s'. Keeping '%s'.",
            name, _current_theme_name
        )


def get_color(key: str) -> Tuple[int, ...]:
    """
    Retrieve a color value for a given semantic key from the active theme.

    Args:
        key (str): Color semantic identifier defined in the theme dictionaries.

    Returns:
        Tuple[int, ...]: RGB or RGBA color tuple. Returns magenta (255,0,255)
        if the key is not present in the active theme.
    """
    return _current_theme.get(key, (255, 0, 255))  # Magenta signals missing key


def get_theme() -> Dict[str, Tuple[int, ...]]:
    """
    Get the full active theme dictionary mapping keys to color tuples.

    Returns:
        Dict[str, Tuple[int, ...]]: Active theme color mapping.
    """
    return _current_theme


def get_theme_name() -> str:
    """
    Retrieve the name of the currently active theme.

    Returns:
        str: Active theme name.
    """
    return _current_theme_name


def random_color() -> Tuple[int, int, int]:
    """
    Generate and return a random RGB color.

    Useful for debugging or visual placeholders when specific theme colors are
    not required.

    Returns:
        Tuple[int, int, int]: A tuple of three integers in [0,255].
    """
    return (
        random.randint(0, 255),  # Red component
        random.randint(0, 255),  # Green component
        random.randint(0, 255),  # Blue component
    )
