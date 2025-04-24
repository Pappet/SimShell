# ui/components/progressbar.py

import pygame
import setup.config as Config
from themes.theme_manager import get_color
from ui.components.base import UIElement

class ProgressBar(UIElement):
    """
    UI element that displays a progress bar for a value between 0 and max_value.
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
    ):
        """
        Initialize the progress bar.

        Args:
            x (int): X position.
            y (int): Y position.
            width (int): Bar width.
            height (int): Bar height.
            current_value (float): Initial fill value.
            max_value (float): Maximum fill value.
            color_key (str): Theme key for fill color.
        """
        super().__init__(x, y, width, height)
        self.current_value = current_value
        self.max_value = max_value
        self.color_key = color_key

    def draw(self, surface: pygame.Surface):
        """
        Draw the progress bar with dynamic theme colors.
        """
        fill_ratio = 0 if self.max_value == 0 else (self.current_value / self.max_value)
        fill_width = int(fill_ratio * self.rect.width)

        fill_color = get_color(self.color_key)
        border_color = get_color("border")

        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(surface, fill_color, fill_rect)
        pygame.draw.rect(
            surface,
            border_color,
            self.rect,
            Config.ui["default"]["border_width"]
        )

    def set_value(self, value: float):
        """
        Set the current value, clamped between 0 and max_value.
        """
        self.current_value = max(0, min(self.max_value, value))
