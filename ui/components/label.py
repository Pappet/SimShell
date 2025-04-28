"""
Module ui/components/label.py

Defines Label UIElement for rendering static text on screen with dynamic theming.
Handles text sizing, color retrieval, and repositioning based on content changes.
"""

import pygame
from typing import Tuple

import setup.config as Config
from themes.theme_manager import get_color
from ui.components.base import UIElement


class Label(UIElement):
    """
    UI element for displaying text labels.

    Attributes:
        text (str): The current text content of the label.
        font (pygame.font.Font): Font used for rendering text.
        color_key (str): Theme key defining the color of the text.
    """
    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        font_size: int = None,
        font_name: str = None
    ) -> None:
        """
        Initialize a new Label instance.

        Args:
            text (str): Text to render.
            x (int): X-coordinate of label position.
            y (int): Y-coordinate of label position.
            font_size (int, optional): Font size in points; uses default if None.
            font_name (str, optional): Font family name; uses default if None.
        """
        # Determine font settings with fallbacks to Config defaults
        font_name = font_name or Config.fonts["default"]["name"]
        font_size = font_size or Config.fonts["default"]["size"]

        # Create font and render initial text to calculate size
        font = pygame.font.SysFont(font_name, font_size)
        text_surf = font.render(text, True, get_color("foreground"))
        width, height = text_surf.get_size()

        # Initialize base UIElement with computed size
        super().__init__(x, y, width, height)

        self.text = text
        self.font = font
        self.color_key = "foreground"

    def set_text(self, new_text: str) -> None:
        """
        Update the label's text content and resize the bounding rect.

        Args:
            new_text (str): The new text string to display.
        """
        self.text = new_text
        # Render text to determine new dimensions
        text_surf = self.font.render(self.text, True, get_color(self.color_key))
        w, h = text_surf.get_size()
        # Update element size and hitbox
        self.width, self.height = w, h
        self.rect.size = (w, h)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Render the label text onto the given surface using current theme.

        Args:
            surface (pygame.Surface): Target surface for drawing.
        """
        color = get_color(self.color_key)
        # Render text and blit at the element's position
        text_surf = self.font.render(self.text, True, color)
        surface.blit(text_surf, self.rect.topleft)
