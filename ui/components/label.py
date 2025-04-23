# ui/components/label.py

import pygame
from themes.theme_manager import get_color
from ui.components.base import UIElement
import setup.config as Config

class Label(UIElement):
    def __init__(
        self,
        text: str,
        position: tuple[int, int],
        font_size: int = None,
        font_name: str = None
    ):
        # Defaults aus eurer Config.fonts
        font_name = font_name or Config.fonts["default"]["name"]
        font_size = font_size or Config.fonts["default"]["size"]

        # Font erzeugen und Text einmal zum Messen rendern
        font = pygame.font.SysFont(font_name, font_size)
        text_surf = font.render(text, True, get_color("foreground"))
        width, height = text_surf.get_size()

        # super init mit Position und gemessener Größe
        x, y = position
        super().__init__(x, y, width, height)

        # State speichern
        self.text = text
        self.font = font
        self.color_key = "foreground"

    def set_text(self, new_text: str):
        """Text ändern und Größe/Rect anpassen."""
        self.text = new_text
        text_surf = self.font.render(self.text, True, get_color(self.color_key))
        w, h = text_surf.get_size()
        self.width, self.height = w, h
        self.rect.size = (w, h)

    def draw(self, surface: pygame.Surface):
        """Jedes Frame neu in aktueller Theme-Farbe rendern."""
        color = get_color(self.color_key)
        text_surf = self.font.render(self.text, True, color)
        surface.blit(text_surf, self.rect.topleft)
