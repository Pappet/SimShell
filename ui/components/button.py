import pygame
import core.config as Config
import utility.color as Color


class Button:
    def __init__(self, rect, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.font = pygame.font.SysFont(Config.FONT_NAME, Config.FONT_SIZE)
        self.hovered = False

    def draw(self, surface):
        color = Color.BUTTON_DEFAULT if self.hovered else Color.BUTTON_HOVER
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, Color.BORDER, self.rect, 2)
        text_surf = self.font.render(self.text, True, Color.BUTTON_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)