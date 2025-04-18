import pygame
import setup.config as Config
from themes.theme_manager import get_color, random_color

class ProgressBar:
    def __init__(self, x, y, w, h, current_value, max_value, color=random_color()):
        self.rect = pygame.Rect(x, y, w, h)
        self.max_value = max_value
        self.current_value = current_value
        self.color = color

    def draw(self, surface):
        fill_width = int((self.current_value / self.max_value) * self.rect.width)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(surface, self.color, fill_rect)
        pygame.draw.rect(surface, get_color("border"), self.rect, Config.ui["default"]["border_width"])

    def set_value(self, value):
        self.current_value = max(0, min(self.max_value, value))
