# themes/theme_manager.py

import random
from themes import dark_theme, light_theme

# Dictionary of available themes
THEMES = {
    "dark": dark_theme.theme,
    "light": light_theme.theme,
}

# Active theme – default is dark
_current_theme = THEMES["dark"]

def set_theme(name: str):
    """
    Sets the active theme by name.

    Args:
        name (str): Name of the theme to activate ("dark" or "light").
    """
    global _current_theme
    _current_theme = THEMES.get(name, _current_theme)

def get_color(key: str):
    """
    Retrieves a color value by key from the current theme.

    Args:
        key (str): Semantic color name.

    Returns:
        tuple: RGB or RGBA color.
    """
    return _current_theme.get(key, (255, 0, 255))  # fallback: bright magenta = "missing"

def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)