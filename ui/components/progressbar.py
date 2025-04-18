import pygame
import utility.color as Color

class ProgressBar:
    def __init__(self, x, y, w, h, max_value, color=Color.random_color()):
        self.rect = pygame.Rect(x, y, w, h)
        self.max_value = max_value
        self.current_value = max_value
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, Color.BLACK, self.rect, 2)
        fill_width = int((self.current_value / self.max_value) * self.rect.width)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(surface, self.color, fill_rect)

    def set_value(self, value):
        self.current_value = max(0, min(self.max_value, value))
