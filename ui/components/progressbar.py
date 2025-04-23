# ui/components/progressbar.py

import pygame
import setup.config as Config
from themes.theme_manager import get_color
from ui.components.base import UIElement

class ProgressBar(UIElement):
    def __init__(self, x, y, w, h, current_value, max_value, color=None):
        # super kümmert sich um rect und Position
        super().__init__(x, y, w, h)

        self.max_value = max_value
        self.current_value = current_value
        # wenn keine Farbe übergeben, Default aus Theme
        self.color = color or get_color("progress_fill")

    def draw(self, surface):
        # gefüllter Bereich
        pct = 0 if self.max_value == 0 else (self.current_value / self.max_value)
        fill_w = int(pct * self.rect.width)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_w, self.rect.height)
        pygame.draw.rect(surface, self.color, fill_rect)
        # Rahmen
        pygame.draw.rect(surface,
                         get_color("border"),
                         self.rect,
                         Config.ui["default"]["border_width"])

    def set_value(self, value):
        self.current_value = max(0, min(self.max_value, value))
