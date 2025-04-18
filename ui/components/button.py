import pygame
from core.config import FONT_SIZE, FONT_NAME
import utility.color as Color


class Button:
    def __init__(self, rect, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.hovered = False

    def draw(self, surface):
        color = Color.DARK_GRAY if self.hovered else Color.GRAY
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, Color.BLACK, self.rect, 2)
        text_surf = self.font.render(self.text, True, Color.BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)