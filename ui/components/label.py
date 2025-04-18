import pygame
import utility.color as Color
from core.config import FONT_SIZE, FONT_NAME

class Label:
    def __init__(self, text, position):
        self.text = text
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.color = Color.BLACK
        text_surf = self.font.render(self.text, True, self.color)
        self.rect = text_surf.get_rect(topleft=position)

    def set_text(self, new_text):
        self.text = new_text
        text_surf = self.font.render(self.text, True, self.color)
        self.rect.width = text_surf.get_width()
        self.rect.height = text_surf.get_height()

    def draw(self, surface):
        text_surf = self.font.render(self.text, True, self.color)
        surface.blit(text_surf, self.rect.topleft)