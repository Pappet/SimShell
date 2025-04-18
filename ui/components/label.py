import pygame
from themes.theme_manager import get_color
import core.config as Config

class Label:
    def __init__(self, text, position):
        self.text = text
        self.font = pygame.font.SysFont(Config.FONT_NAME, Config.FONT_SIZE)
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