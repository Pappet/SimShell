import random

"""
Defines semantic color roles for the UI in NoMapNeeded.
These colors can be easily adjusted to implement themes (e.g. light/dark mode).
"""

# General UI layout colors
BACKGROUND      = (24, 24, 24)       # Main background (dark gray)
FOREGROUND      = (230, 230, 230)    # Standard text
PANEL_BG        = (40, 40, 40)       # Panels, windows
BORDER          = (100, 100, 100)    # Panel outlines or dividers

# Buttons
BUTTON_DEFAULT  = (60, 60, 60)
BUTTON_HOVER    = (90, 90, 90)
BUTTON_ACTIVE   = (110, 110, 110)
BUTTON_TEXT     = (255, 255, 255)

# Status / Messaging
SUCCESS         = (0, 200, 100)      # Green - success
WARNING         = (255, 204, 0)      # Yellow - caution
ERROR           = (200, 50, 50)      # Red - error or danger
INFO            = (0, 180, 255)      # Cyan - neutral info

# Accents / highlights
HIGHLIGHT       = (255, 102, 0)      # Orange - attention/highlight
SELECTION       = (80, 120, 255)     # Blue - selected item

# Utility
TRANSPARENT     = (0, 0, 0, 0)
TRANSPARENT_50  = (0, 0, 0, 128)     # Semi-transparent black
WHITE           = (255, 255, 255)
BLACK           = (0, 0, 0)

# Color roles for the game world
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

def theme_as_dict():
    """
    Returns the theme as a dictionary, useful for theme switching or exporting.

    Returns:
        dict[str, tuple[int, int, int]]: A mapping of semantic color roles to RGB values.
    """
    return {
        "background": BACKGROUND,
        "foreground": FOREGROUND,
        "panel_bg": PANEL_BG,
        "border": BORDER,
        "button_default": BUTTON_DEFAULT,
        "button_hover": BUTTON_HOVER,
        "button_active": BUTTON_ACTIVE,
        "button_text": BUTTON_TEXT,
        "success": SUCCESS,
        "warning": WARNING,
        "error": ERROR,
        "info": INFO,
        "highlight": HIGHLIGHT,
        "selection": SELECTION,
        "transparent": TRANSPARENT,
        "white": WHITE,
        "black": BLACK,
    }

def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)