# Module themes/dracula_theme.py
#
# Defines the Dracula UI color theme inspired by the Dracula coding theme.
# Provides semantic color keys mapped to RGB(A) tuples for use in the ThemeManager.

theme = {
    # Core UI colors
    "background": (40, 42, 54),           # Dracula Hintergrund (#282a36)
    "foreground": (248, 248, 242),        # Hellgrauer Text (#f8f8f2)
    "panel_bg": (68, 71, 90),             # Aktuelle Zeile / Panels (#44475a)
    "border": (68, 71, 90),               # Gleicher Ton für Rahmen (#44475a)

    # Console overlay (semi-transparent für subtile Effekte)
    "background_console": (40, 42, 54, 200),  # Semi-transparent Dracula-Hintergrund
    "foreground_console": (80, 250, 123),     # Grün für Konsole (#50fa7b)

    # Button states
    "button_default": (68, 71, 90),       # Panel-Farbe für Buttons
    "button_hover": (98, 100, 118),       # Aufgehellt für Hover
    "button_active": (139, 133, 189),     # Lila-active (#8d79d6 angenähert)
    "button_text": (248, 248, 242),       # Weißer Button-Text

    # Checkbox styling
    "checkbox_box": (98, 100, 118),       # Platzhalter-Kästchen (#6272a4 angenähert)
    "checkbox_check": (80, 250, 123),     # Grün für Häkchen
    "label_text": (189, 147, 249),        # Lila Labels (#bd93f9)

    # Input field styling
    "input_bg": (68, 71, 90),             # Panels-Hintergrund
    "input_text": (248, 248, 242),        # Weißer Input-Text
    "input_placeholder": (98, 100, 118),  # Gedimmtes Placeholder
    "input_cursor": (255, 121, 198),      # Pinker Cursor (#ff79c6)

    # Focus indicator
    "focus_glow": (189, 147, 249),        # Lila Glow

    # Status indicators (Dracula-Hues)
    "success": (80, 250, 123),            # Grün (#50fa7b)
    "warning": (241, 250, 140),           # Gelb (#f1fa8c)
    "error": (255, 85, 85),               # Rot (#ff5555)
    "info": (139, 233, 253),              # Cyan (#8be9fd)
    "highlight": (255, 121, 198),         # Pink (#ff79c6)
    "selection": (98, 100, 118),          # Markdown-Selection (#6272a4 angenähert)

    # Utility colors
    "transparent": (0, 0, 0, 0),          # Voll transparent
    "transparent_50": (0, 0, 0, 128),     # 50% transparent
    "white": (255, 255, 255),             # Weiß
    "black": (0, 0, 0),                   # Schwarz

    # Game-specific stat bars
    "energy": (241, 250, 140),            # Gelb für Energie
    "health": (255, 85, 85),              # Rot für Gesundheit
    "mana": (139, 233, 253),              # Cyan für Mana
}
