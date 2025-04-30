"""
Module themes/light_theme.py

Defines the light UI color theme with semantic color keys mapped to RGB(A) tuples.
Used by the ThemeManager to style UI elements consistently in light mode.
"""

# Light theme color definitions
# Each key corresponds to a semantic usage in the UI (backgrounds, text, alerts, etc.)

theme = {
    # Core background and foreground
    "background": (245, 245, 245),         # Main window background (light gray)
    "foreground": (30, 30, 30),            # Default text color (dark gray)

    # Panel styling
    "panel_bg": (225, 225, 225),           # Panel/dialog background (very light gray)
    "border": (150, 150, 150),             # Borders and dividers (medium gray)

    # Console overlay colors (RGBA)
    "background_console": (0, 0, 0, 128),  # Semi-transparent black console background
    "foreground_console": (0, 255, 0),     # Neon green console text

    # Button states
    "button_default": (230, 230, 230),     # Default button fill (very light gray)
    "button_hover": (210, 210, 210),       # Hovered button fill (slightly darker)
    "button_active": (190, 190, 190),      # Pressed button fill (darker gray)
    "button_text": (0, 0, 0),              # Button label text (black)

    # Checkbox styling
    "checkbox_box": (200, 200, 200),       # Checkbox box background (light gray)
    "checkbox_check": (50, 150, 50),       # Checkbox tick/fill color (green)

    # Label text
    "label_text": (0, 0, 0),               # Labels and static text (black)

    # Input field colors
    "input_bg": (255, 255, 255),           # Input background (white)
    "input_text": (0, 0, 0),               # Typed text (black)
    "input_placeholder": (150, 150, 150),  # Placeholder text (gray)
    "input_cursor": (0, 0, 0),             # Text cursor color (black)

    # Focus indicator
    "focus_glow": (255, 255, 0),           # Glow outline for focused elements (yellow)

    # Status indicators
    "success": (0, 200, 100),              # Success messages (green)
    "warning": (255, 204, 0),              # Warning or caution (yellow)
    "error": (200, 50, 50),                # Error or critical (red)
    "info": (0, 180, 255),                 # Informational messages (cyan)
    "highlight": (255, 102, 0),            # Highlights or accents (orange)
    "selection": (100, 140, 255),          # Selected items (blue)

    # Utility colors
    "transparent": (0, 0, 0, 0),           # Fully transparent
    "transparent_50": (255, 255, 255, 128),# 50% transparent white
    "white": (255, 255, 255),              # Pure white
    "black": (0, 0, 0),                    # Pure black

    # Game-specific stat colors
    "energy": (255, 255, 0),               # Energy bar/fill (yellow)
    "health": (255, 0, 0),                 # Health bar/fill (red)
    "mana": (0, 0, 255),                   # Mana bar/fill (blue)
}