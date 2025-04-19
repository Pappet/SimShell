# core/debug_console.py

'''
Debug Console for logging messages in a Pygame application.
This console can be used to display logs, errors, or any other messages
during the game's execution.
It can be drawn on the screen and supports a maximum number of lines to display.
'''

import pygame
import setup.config as Config
from themes.theme_manager import get_color


class DebugConsole:
    def __init__(self, font: pygame.font.Font, max_lines=Config.ui["debug_console"]["max_lines"], color=get_color("foreground_console")):
        self.font = font
        self.logs = []
        self.max_lines = max_lines
        self.color = color

    def log(self, message):
        """Adds the time and the log line."""
        time = pygame.time.get_ticks() // 1000
        self.logs.append(str(f"{time}: {message}"))
        if len(self.logs) > self.max_lines:
            self.logs.pop(0)

    def clear(self):
        """Clears the console."""
        self.logs.clear()

    def draw(self, surface, pos=(10, 10)):
        """Draws the console with a semi-transparent background."""
        self.color = get_color("foreground_console")
        x, y = pos

        # Maße für den Hintergrund ermitteln
        line_height = self.font.get_linesize()
        padding = Config.ui["default"]["padding"]
        bg_width = 0
        for log in self.logs:
            text_w, _ = self.font.size(log)
            bg_width = max(bg_width, text_w)
        bg_width += padding * 2
        bg_height = line_height * len(self.logs) + padding * 2 + (len(self.logs) - 1) * 2

        # Surface mit Alphakanal erstellen
        bg_surf = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        
        # Füllfarbe mit Alpha (z.B. schwarz mit 128/255 Alpha)
        bg_surf.fill(get_color("background_console"))

        # Hintergrund auf das Ziel‑Surface blitten
        surface.blit(bg_surf, (x - padding, y - padding))

        # Logs drüber zeichnen
        y_offset = y
        for log in self.logs:
            text_surf = self.font.render(log, True, self.color)
            surface.blit(text_surf, (x, y_offset))
            y_offset += line_height + 2

