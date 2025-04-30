"""
Module themes/dark_theme.py

Defines the dark UI color theme with semantic color keys mapped to RGB(A) tuples.
Used by the ThemeManager to style UI elements consistently in dark mode.
"""

# Dark theme color definitions
# Each key corresponds to a semantic usage in the UI (e.g., backgrounds, text, alerts)

theme = {
    # Core background and foreground
    "background": (24, 24, 24),         # Main window background (very dark gray)
    "foreground": (230, 230, 230),      # Default text color (light gray)

    # Panel styling
    "panel_bg": (40, 40, 40),           # Panel and dialog backgrounds (dark gray)
    "border": (100, 100, 100),          # Borders and dividers (medium gray)

    # Console overlay colors (RGBA)
    "background_console": (0, 0, 0, 128),  # Semi-transparent black console background
    "foreground_console": (0, 255, 0),     # Neon green text for console output

    # Button states
    "button_default": (60, 60, 60),     # Default button fill (dark gray)
    "button_hover": (90, 90, 90),       # Hovered button fill (light gray)
    "button_active": (110, 110, 110),   # Active/pressed button fill (lighter gray)
    "button_text": (255, 255, 255),     # Button label text (white)

    # Checkbox styling
    "checkbox_box": (200, 200, 200),    # Checkbox box background (light gray)
    "checkbox_check": (50, 150, 50),    # Checkbox tick/fill color (green)

    # Label text
    "label_text": (255, 255, 255),      # Labels and static text (white)

    # Input field colors
    "input_bg": (255, 255, 255),        # Input background (white)
    "input_text": (0, 0, 0),            # Typed text (black)
    "input_placeholder": (150, 150, 150),# Placeholder text (gray)
    "input_cursor": (0, 0, 0),          # Text cursor color (black)

    # Focus indicator
    "focus_glow": (255, 255, 0),        # Glow outline for focused elements (yellow)

    # Status indicators
    "success": (0, 200, 100),           # Success messages (green)
    "warning": (255, 204, 0),           # Warning or caution (yellow)
    "error": (200, 50, 50),             # Error or critical (red)
    "info": (0, 180, 255),              # Informational messages (cyan)
    "highlight": (255, 102, 0),         # Highlights or accents (orange)
    "selection": (80, 120, 255),        # Selected items (blue)

    # Utility colors
    "transparent": (0, 0, 0, 0),        # Fully transparent
    "transparent_50": (0, 0, 0, 128),   # 50% transparent black
    "white": (255, 255, 255),           # Pure white
    "black": (0, 0, 0),                 # Pure black

    # Game-specific stat colors
    "energy": (255, 255, 0),            # Energy bar/fill (yellow)
    "health": (255, 0, 0),              # Health bar/fill (red)
    "mana": (0, 0, 255),                # Mana bar/fill (blue)
}
