# themes/theme_manager.py

"""
Theme manager for loading and switching UI color themes.
"""

import random
from typing import Dict, Tuple, Any
from themes import dark_theme, light_theme, retro_theme
import setup.config as Config

# Mapping of theme names to their color dictionaries
THEMES: Dict[str, Dict[str, Tuple[int, ...]]] = {
    "dark": dark_theme.theme,
    "light": light_theme.theme,
    "retro": retro_theme.theme,
}

# Active theme is set based on Config.theme['default']
_current_theme: Dict[str, Tuple[int, ...]] = THEMES.get(
    Config.theme.get("default", "dark"),
    dark_theme.theme
)
_current_theme_name: str = Config.theme.get("default", "dark")


def set_theme(name: str) -> None:
    """
    Set the active UI theme by name.

    Args:
        name (str): One of the keys in THEMES (e.g. "dark", "light", "retro").
    """
    global _current_theme, _current_theme_name
    if name in THEMES:
        _current_theme = THEMES[name]
        _current_theme_name = name
    else:
        # If theme name is invalid, keep current theme
        pass


def get_color(key: str) -> Tuple[int, ...]:
    """
    Retrieve a color tuple from the current theme.

    Args:
        key (str): Semantic color key defined in the theme.

    Returns:
        Tuple[int, ...]: RGB or RGBA color. Returns magenta (255,0,255) if key is missing.
    """
    return _current_theme.get(key, (255, 0, 255))


def get_theme() -> Dict[str, Tuple[int, ...]]:
    """
    Return the entire active theme dictionary.

    Returns:
        Dict[str, Tuple[int, ...]]: Mapping of color keys to color tuples.
    """
    return _current_theme


def get_theme_name() -> str:
    """
    Get the name of the currently active theme.

    Returns:
        str: Current theme name (e.g. "dark").
    """
    return _current_theme_name


def random_color() -> Tuple[int, int, int]:
    """
    Generate a random RGB color tuple.

    Returns:
        Tuple[int, int, int]: Random color.
    """
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
