"""
Module ui/components/button.py

Defines Button UIElement for clickable buttons with hover effects and click callbacks.
Integrates with EventManager to dispatch UI_BUTTON_CLICKED events and optionally
plays a sound on click.
"""

import logging
import pygame

import setup.config as Config
from themes.theme_manager import get_color
from core.events.event_types import EventType
from ui.components.base import UIElement

logger = logging.getLogger(__name__)


class Button(UIElement):
    """
    Clickable button component with hover highlighting and callback invocation.

    Attributes:
        text (str): Label displayed on the button.
        callback (callable): Function executed when the button is clicked.
        event_manager (EventManager | None): Optional event manager for dispatching UI_BUTTON_CLICKED.
        sound_key (str | None): Optional key for playing a click sound via SoundManager.
        hovered (bool): Indicates whether the mouse is currently over the button.
        font (pygame.font.Font): Font used to render the button label.
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
    ) -> None:
        """
        Initialize a new Button instance.

        Args:
            x (int): X-coordinate of the button's top-left corner.
            y (int): Y-coordinate of the button's top-left corner.
            width (int): Width of the button in pixels.
            height (int): Height of the button in pixels.
            text (str): Text label shown on the button.
            callback (callable): Function to call when button is clicked.
            event_manager (EventManager, optional): Used to dispatch click events.
            sound_key (str, optional): Key to identify the click sound in SoundManager.
        """
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback
        self.event_manager = event_manager
        self.sound_key = sound_key
        self.hovered = False

        # Configure font for button label
        font_cfg = Config.fonts["default"]
        self.font = pygame.font.SysFont(
            font_cfg["name"], font_cfg["size"]
        )
        logger.debug("Button initialized at (%d, %d) size (%d,%d) with text '%s'", x, y, width, height, text)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Render the button rectangle, border, and centered label.
        Changes background color on hover state.

        Args:
            surface (pygame.Surface): The target surface for drawing.
        """
        # Select theme colors for default and hover states
        bg_key = "button_hover" if self.hovered else "button_default"
        bg_color = get_color(bg_key)
        border_color = get_color("border")
        text_color = get_color("button_text")

        # Draw button background and border
        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(
            surface,
            border_color,
            self.rect,
            Config.ui["default"]["border_width"]
        )

        # Render and center the text label
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Process mouse click events and invoke callbacks on left-button down.
        Dispatches a UI_BUTTON_CLICKED event via event_manager and plays sound if configured.

        Args:
            event (pygame.event.Event): The Pygame event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                # Execute the assigned callback
                try:
                    self.callback()
                except Exception:
                    logger.exception("Error executing button callback for '%s'", self.text)

                # Dispatch click event to EventManager
                if self.event_manager:
                    self.event_manager.dispatch(EventType.UI_BUTTON_CLICKED, self)
            
    def update(self, mouse_pos: tuple[int, int]) -> None:
        """
        Update the hovered state based on the current mouse position.

        Args:
            mouse_pos (tuple[int, int]): The (x, y) coordinates of the mouse pointer.
        """
        self.hovered = self.rect.collidepoint(mouse_pos)
        #logger.debug("Button '%s' hover state: %s", self.text, self.hovered)
