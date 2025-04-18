import pygame
import core.config as Config
from themes.theme_manager import get_color

class Button:
    def __init__(self, rect, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.font = pygame.font.SysFont(Config.FONT_NAME, Config.FONT_SIZE)
        self.hovered = False

    def draw(self, surface):
        color = get_color("button_default") if self.hovered else get_color("button_hover")
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, get_color("border"), self.rect, 2)
        text_surf = self.font.render(self.text, True, get_color("button_text"))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)