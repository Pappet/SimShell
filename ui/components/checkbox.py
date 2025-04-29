# ui/components/checkbox.py

"""
Defines UICheckbox UIElement for toggling boolean values via mouse clicks.
Optionally calls a callback when toggled.
"""

import pygame
import logging
from ui.components.base import UIElement
from themes.theme_manager import get_color
import setup.config as Config

logger = logging.getLogger(__name__)

class UICheckbox(UIElement):
    """
    UI element for a clickable checkbox with optional label and callback.

    Attributes:
        checked (bool): Whether the checkbox is checked.
        callback (callable): Optional function called when toggled.
        label (str): Optional text label displayed next to the checkbox.
    """
    def __init__(
        self,
        x: int,
        y: int,
        label: str = "",
        checked: bool = False,
        callback: callable = None
    ) -> None:
        """
        Initialize a UICheckbox element.

        Args:
            x (int): X coordinate.
            y (int): Y coordinate.
            label (str, optional): Text label to show next to checkbox.
            checked (bool, optional): Initial checked state.
            callback (callable, optional): Function to call when toggled.
        """
        size = Config.ui["checkbox"]["size"]  # e.g. 20px
        super().__init__(x, y, size, size)
        self.checked = checked
        self.callback = callback
        self.label = label

        font_cfg = Config.fonts["default"]
        self.font = pygame.font.SysFont(
            font_cfg["name"], font_cfg["size"]
        )

        logger.debug(f"UICheckbox initialized at ({x},{y}) with label '{label}' checked={checked}")

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the checkbox and optional label.

        Args:
            surface (pygame.Surface): Surface to draw on.
        """
        box_color = get_color("checkbox_box")
        check_color = get_color("checkbox_check")
        border_color = get_color("border")
        text_color = get_color("label_text")

        # Draw checkbox box
        pygame.draw.rect(surface, box_color, self.rect)
        pygame.draw.rect(
            surface, border_color, self.rect, Config.ui["default"]["border_width"]
        )

        # Draw checkmark if checked
        if self.checked:
            padding = 4
            inner_rect = self.rect.inflate(-padding, -padding)
            pygame.draw.rect(surface, check_color, inner_rect)

        # Draw label text if present
        if self.label:
            text_surf = self.font.render(self.label, True, text_color)
            text_rect = text_surf.get_rect(midleft=(self.rect.right + 10, self.rect.centery))
            surface.blit(text_surf, text_rect)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Toggle checkbox state on mouse click.

        Args:
            event (pygame.event.Event): Event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked
                logger.debug(f"UICheckbox '{self.label}' toggled to {self.checked}")
                if self.callback:
                    try:
                        self.callback(self.checked)
                    except Exception:
                        logger.exception(f"Error in checkbox callback for '{self.label}'")

    def update(self, mouse_pos: tuple[int, int]) -> None:
        """
        Nothing dynamic yet. Hover effects could be added here.
        """
        pass
