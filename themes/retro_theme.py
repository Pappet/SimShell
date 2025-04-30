# themes/retro_theme.py

# Retro theme inspired by classic EGA/CGA palettes and CRT monitor aesthetics

theme = {
    # Core UI colors
    "background": (0, 0, 0),           # Black background (CRT off-state)
    "foreground": (255, 255, 255),     # White text (EGA default)
    "panel_bg": (32, 32, 32),          # Dark gray panels
    "border": (128, 128, 128),         # Gray borders

    # Console overlay
    "background_console": (0, 0, 0, 200),  # Semi-transparent black for console
    "foreground_console": (0, 255, 0),     # Neon green console text

    # Buttons
    "button_default": (64, 64, 64),     # Dark gray buttons
    "button_hover": (96, 96, 96),       # Gray hover state
    "button_active": (160, 160, 160),   # Light gray active state
    "button_text": (255, 255, 0),       # Yellow text for buttons

    #Checkbox
    "checkbox_box": (200, 200, 200),
    "checkbox_check": (50, 150, 50),
    "label_text": (255, 255, 0),

    #Input Box
    "input_bg": (255, 255, 255),
    "input_text": (0, 0, 0),
    "input_placeholder": (150, 150, 150),
    "input_cursor": (0, 0, 0),

    # Status indicators
    "success": (0, 255, 0),           # Green - success
    "warning": (255, 255, 0),         # Yellow - caution
    "error": (255, 0, 0),             # Red - error
    "info": (0, 0, 255),              # Blue - informational
    "highlight": (255, 0, 255),       # Magenta - highlight/attention
    "selection": (0, 255, 255),       # Cyan - selected items

    # Transparency shorthands
    "transparent": (0, 0, 0, 0),      # Fully transparent
    "transparent_50": (0, 0, 0, 128), # Semi-transparent black
    "white": (255, 255, 255),         # White
    "black": (0, 0, 0),               # Black

    # Game/resource bars
    "energy": (255, 255, 0),          # Yellow - energy
    "health": (255, 0, 0),            # Red - health
    "mana": (0, 0, 255),              # Blue - mana
}
