"""
Module ui/components/progressbar.py

Defines ProgressBar UIElement for visualizing a value's progress relative to a maximum.
Renders filled portion, border, and provides methods to update the current value safely.
"""

import pygame
from typing import Tuple

import setup.config as Config
from themes.theme_manager import get_color
from ui.components.base import UIElement


class ProgressBar(UIElement):
    """
    UI element that displays a horizontal progress bar indicating a value proportion.

    Attributes:
        current_value (float): The current measured value.
        max_value (float): The maximum value the bar represents when full.
        color_key (str): Theme key for the fill color of the bar.
    """
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        current_value: float,
        max_value: float,
        color_key: str = "progress_fill"
    ) -> None:
        """
        Initialize a ProgressBar instance.

        Args:
            x (int): X-coordinate of the bar's top-left corner.
            y (int): Y-coordinate of the bar's top-left corner.
            width (int): Total width of the bar in pixels.
            height (int): Height of the bar in pixels.
            current_value (float): Starting fill value.
            max_value (float): Value corresponding to a completely filled bar.
            color_key (str, optional): Theme key for the fill color.
        """
        super().__init__(x, y, width, height)
        self.current_value = current_value
        self.max_value = max_value
        self.color_key = color_key

    def draw(self, surface: pygame.Surface) -> None:
        """
        Render the progress bar's filled portion and border on the surface.

        Calculates fill width based on current vs. max values, applies theme colors.

        Args:
            surface (pygame.Surface): The target surface to draw on.
        """
        # Compute fill ratio and pixel width for the filled area
        fill_ratio = 0.0 if self.max_value == 0 else (self.current_value / self.max_value)
        fill_width = int(fill_ratio * self.rect.width)

        # Retrieve theme colors
        fill_color = get_color(self.color_key)
        border_color = get_color("border")

        # Draw filled rectangle and border
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(surface, fill_color, fill_rect)
        pygame.draw.rect(
            surface,
            border_color,
            self.rect,
            Config.ui["default"]["border_width"]
        )

    def set_value(self, value: float) -> None:
        """
        Update the bar's current value, clamped between 0 and max_value.

        Args:
            value (float): The new value to represent.
        """
        # Clamp value to valid range
        self.current_value = max(0.0, min(self.max_value, value))
