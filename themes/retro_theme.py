"""
Module themes/retro_theme.py

Defines the retro UI color theme inspired by classic EGA/CGA palettes and CRT monitor aesthetics.
Provides semantic color keys mapped to RGB(A) tuples for use in the ThemeManager.
"""

# Retro theme color definitions
# Emulates old-school computer display palettes with high-contrast blocks

theme = {
    # Core UI colors
    "background": (0, 0, 0),           # Black background (CRT off-state)
    "foreground": (255, 255, 255),     # White text (EGA default)
    "panel_bg": (32, 32, 32),          # Dark gray panel backgrounds
    "border": (128, 128, 128),         # Medium gray borders

    # Console overlay (opaque for retro effect)
    "background_console": (0, 0, 0, 200),  # Semi-transparent black
    "foreground_console": (0, 255, 0),     # Neon green console text

    # Button states
    "button_default": (64, 64, 64),     # Dark gray buttons
    "button_hover": (96, 96, 96),       # Hover state buttons
    "button_active": (160, 160, 160),   # Active/pressed state
    "button_text": (255, 255, 0),       # Yellow text for buttons (CGA palette)

    # Checkbox styling
    "checkbox_box": (200, 200, 200),    # Light gray checkbox box
    "checkbox_check": (50, 150, 50),    # Green check fill
    "label_text": (255, 255, 0),        # Yellow labels

    # Input field styling
    "input_bg": (255, 255, 255),        # White input background
    "input_text": (0, 0, 0),            # Black input text
    "input_placeholder": (150, 150, 150),# Gray placeholder
    "input_cursor": (0, 0, 0),          # Black cursor

    # Focus indicator
    "focus_glow": (255, 255, 0),        # Yellow glow for focus

    # Status indicators (solid retro hues)
    "success": (0, 255, 0),             # Bright green success
    "warning": (255, 255, 0),           # Bright yellow warning
    "error": (255, 0, 0),               # Bright red error
    "info": (0, 0, 255),                # Bright blue informational
    "highlight": (255, 0, 255),         # Magenta highlight
    "selection": (0, 255, 255),         # Cyan selection

    # Utility colors
    "transparent": (0, 0, 0, 0),        # Fully transparent
    "transparent_50": (0, 0, 0, 128),   # Semi-transparent black
    "white": (255, 255, 255),           # White
    "black": (0, 0, 0),                 # Black

    # Game-specific stat bars
    "energy": (255, 255, 0),            # Yellow energy bar
    "health": (255, 0, 0),              # Red health bar
    "mana": (0, 0, 255),                # Blue mana bar
}