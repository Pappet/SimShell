# ui/components/button.py

import pygame
import setup.config as Config
from themes.theme_manager import get_color
from ui.components.base import UIElement

class Button(UIElement):
    def __init__(self, rect, text, callback):
        # unpack rect und rufe UIElement.__init__ auf
        x, y, width, height = rect
        super().__init__(x, y, width, height)

        self.text = text
        self.callback = callback
        self.hovered = False

        # Font mit euren Config-Konstanten
        self.font = pygame.font.SysFont(
            Config.fonts["default"]["name"],
            Config.fonts["default"]["size"]
        )

    def draw(self, surface):
        # Hover-Farbe richtig wählen
        bg_color = get_color("button_hover")   if self.hovered else \
                   get_color("button_default")
        # Hintergrund
        pygame.draw.rect(surface, bg_color, self.rect)
        # Rahmen
        pygame.draw.rect(
            surface, 
            get_color("border"), 
            self.rect, 
            Config.ui["default"]["border_width"]
        )
        # Text zentriert
        text_surf = self.font.render(self.text, True, get_color("button_text"))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        # Klick-Erkennung
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def update(self, mouse_pos):
        # Mouse-Over Status
        self.hovered = self.rect.collidepoint(mouse_pos)
