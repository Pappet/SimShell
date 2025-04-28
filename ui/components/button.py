import pygame
import setup.config as Config
from themes.theme_manager import get_color
from ui.components.base import UIElement

class Button(UIElement):
    """
    UI button with hover effect and click callback functionality.
    """
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        callback: callable,
        event_manager=None,
        sound_key: str = None
    ):
        """
        Initialize the button.

        Args:
            x (int): X position of the button.
            y (int): Y position of the button.
            width (int): Width of the button.
            height (int): Height of the button.
            text (str): Label text.
            callback (callable): Function to call on click.
            event_manager (EventManager): Event manager for dispatching events.
            sound_key (str): Key for sound effect.
        """
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback
        self.event_manager = event_manager
        self.hovered = False

        font_name = Config.fonts["default"]["name"]
        font_size = Config.fonts["default"]["size"]
        self.font = pygame.font.SysFont(font_name, font_size)
        self.sound_key = sound_key

    def draw(self, surface: pygame.Surface):
        """
        Draw the button with dynamic theme colors.
        """
        bg_key = "button_hover" if self.hovered else "button_default"
        bg_color = get_color(bg_key)
        border_color = get_color("border")
        text_color = get_color("button_text")

        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(
            surface,
            border_color,
            self.rect,
            Config.ui["default"]["border_width"]
        )

        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event: pygame.event.Event):
        """
        Handle mouse click events.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()
                if self.event_manager:
                    from core.events.event_types import EventType
                    self.event_manager.dispatch(EventType.UI_BUTTON_CLICKED, self)

    def update(self, mouse_pos: tuple[int, int]):
        """
        Update hover state based on mouse position.
        """
        self.hovered = self.rect.collidepoint(mouse_pos)
