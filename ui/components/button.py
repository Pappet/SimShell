"""
Module ui/components/button.py

Defines UIButton UIElement for clickable buttons with hover effects, focus handling, and click callbacks.
Integrates with EventManager to dispatch UI_BUTTON_CLICKED events.
"""

import logging
import pygame

import setup.config as Config
from themes.theme_manager import get_color
from core.events.event_types import EventType
from ui.components.base import UIElement

logger = logging.getLogger(__name__)


class UIButton(UIElement):
    """
    Clickable button component with hover highlighting, focus glow, and callback invocation.

    Attributes:
        text (str): Label displayed on the button.
        callback (callable): Function executed when the button is clicked.
        event_manager (EventManager | None): Optional event manager for dispatching UI_BUTTON_CLICKED.
        sound_key (str | None): Optional key for playing a click sound via SoundManager.
        hovered (bool): Indicates whether the mouse is currently over the button.
        focusable (bool): Whether this button can receive keyboard focus.
        focused (bool): Current keyboard focus state.
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
        sound_key: str = None
    ) -> None:
        """
        Initialize a new UIButton instance.

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
        self.event_manager = None
        self.sound_key = sound_key
        self.hovered = False
        self.focusable = True

        # Configure font for button label
        font_cfg = Config.fonts["default"]
        self.font = pygame.font.SysFont(
            font_cfg["name"], font_cfg["size"]
        )
        logger.debug(
            "UIButton initialized at (%d, %d) size (%d,%d) with text '%s'",
            x, y, width, height, text
        )

    def draw(self, surface: pygame.Surface) -> None:
        """
        Render the button rectangle, border, label, and focus glow if focused.
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

        # Draw focus glow
        if self.focused:
            glow_rect = self.rect.inflate(4, 4)
            pygame.draw.rect(surface, get_color("focus_glow"), glow_rect, 2)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Process mouse click events and invoke callbacks on left-button down.
        Dispatches a UI_BUTTON_CLICKED event via event_manager.

        Args:
            event (pygame.event.Event): The Pygame event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                try:
                    self.callback()
                except Exception:
                    logger.exception("Error executing button callback for '%s'", self.text)

                if self.event_manager:
                    self.event_manager.dispatch(EventType.UI_BUTTON_CLICKED, self)

    def update(self, mouse_pos: tuple[int, int]) -> None:
        """
        Update the hovered state based on the current mouse position.

        Args:
            mouse_pos (tuple[int, int]): The (x, y) coordinates of the mouse pointer.
        """
        self.hovered = self.rect.collidepoint(mouse_pos)

    def activate(self) -> None:
        """
        Activate the button when ENTER/SPACE is pressed while focused.
        Invokes the callback function.
        """
        try:
            self.callback()
        except Exception:
            logger.exception("Error activating button callback for '%s'", self.text)