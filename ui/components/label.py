# ui/components/label.py

import pygame
import setup.config as Config
from themes.theme_manager import get_color
from ui.components.base import UIElement

class Label(UIElement):
    """
    Simple text label UI element.
    """
    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        font_size: int = None,
        font_name: str = None
    ):
        """
        Initialize the label.

        Args:
            text (str): Text to display.
            x (int): X position.
            y (int): Y position.
            font_size (int, optional): Font size.
            font_name (str, optional): Font name.
        """
        font_name = font_name or Config.fonts["default"]["name"]
        font_size = font_size or Config.fonts["default"]["size"]

        font = pygame.font.SysFont(font_name, font_size)
        text_surf = font.render(text, True, get_color("foreground"))
        width, height = text_surf.get_size()

        super().__init__(x, y, width, height)

        self.text = text
        self.font = font
        self.color_key = "foreground"

    def set_text(self, new_text: str):
        """
        Change the displayed text and update size.
        """
        self.text = new_text
        text_surf = self.font.render(self.text, True, get_color(self.color_key))
        w, h = text_surf.get_size()
        self.width, self.height = w, h
        self.rect.size = (w, h)

    def draw(self, surface: pygame.Surface):
        """
        Draw the label with dynamic theme color.
        """
        color = get_color(self.color_key)
        text_surf = self.font.render(self.text, True, color)
        surface.blit(text_surf, self.rect.topleft)
