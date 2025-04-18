import pygame
from themes.theme_manager import get_color
import core.config as Config

class Label:
    def __init__(self, text, position, font_size=Config.FONT_SIZE, font_name=Config.FONT_NAME):
        self.text = text
        self.font_size = font_size
        self.font_name = font_name
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        self.color = get_color("foreground")
        text_surf = self.font.render(self.text, True, self.color)
        self.rect = text_surf.get_rect(topleft=position)

    def set_text(self, new_text):
        self.text = new_text
        text_surf = self.font.render(self.text, True, self.color)
        self.rect.width = text_surf.get_width()
        self.rect.height = text_surf.get_height()

    def draw(self, surface):
        self.color = get_color("foreground")
        text_surf = self.font.render(self.text, True, self.color)
        surface.blit(text_surf, self.rect.topleft)