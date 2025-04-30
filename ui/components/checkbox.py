"""
Module ui/components/checkbox.py

Defines the UICheckbox UI element for toggling boolean options via mouse clicks or keyboard activation.
Supports optional text labels and callback invocation on state change.
"""

import logging
import pygame
from ui.components.base import UIElement
from themes.theme_manager import get_color
import setup.config as Config

logger = logging.getLogger(__name__)


class UICheckbox(UIElement):
    """
    Clickable checkbox component with optional label and toggle callback.

    Attributes:
        checked (bool): Current check state (True if checked).
        label (str): Text displayed next to the checkbox.
        callback (Optional[Callable[[bool], None]]): Function called with new state on toggle.
        focusable (bool): Indicates this element can receive keyboard focus.
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
        Initialize a UICheckbox instance.

        Args:
            x (int): X-coordinate of the checkbox's top-left corner.
            y (int): Y-coordinate of the checkbox's top-left corner.
            label (str, optional): Text label to display to the right of the box.
            checked (bool, optional): Initial checked state. Defaults to False.
            callback (callable, optional): Function to call when toggled. Receives new state.
        """
        # Determine size from configuration (e.g., a square size)
        size = Config.ui["checkbox"]["size"]
        super().__init__(x, y, size, size)

        self.checked = checked
        self.callback = callback
        self.label = label
        # Enable keyboard focus navigation for this element
        self.focusable = True

        # Prepare font for optional label text
        font_cfg = Config.fonts["default"]
        self.font = pygame.font.SysFont(font_cfg["name"], font_cfg["size"])

        logger.debug(
            "UICheckbox initialized at (%d,%d) size %d label '%s' checked=%s",
            x, y, size, label, checked
        )

    def draw(self, surface: pygame.Surface) -> None:
        """
        Render the checkbox box, checkmark if checked, optional label, and focus glow.

        Args:
            surface (pygame.Surface): Surface to draw on.
        """
        # Colors based on current theme
        box_color = get_color("checkbox_box")
        check_color = get_color("checkbox_check")
        border_color = get_color("border")
        text_color = get_color("label_text")
        focus_glow = get_color("focus_glow")

        # Draw the checkbox square
        pygame.draw.rect(surface, box_color, self.rect)
        pygame.draw.rect(
            surface,
            border_color,
            self.rect,
            Config.ui["default"]["border_width"]
        )

        # Draw inner checkmark if in checked state
        if self.checked:
            padding = 4
            inner_rect = self.rect.inflate(-padding * 2, -padding * 2)
            pygame.draw.rect(surface, check_color, inner_rect)

        # Draw label text to the right if provided
        if self.label:
            text_surf = self.font.render(self.label, True, text_color)
            text_pos = (
                self.rect.right + 8,
                self.rect.y + (self.rect.height - text_surf.get_height()) // 2
            )
            surface.blit(text_surf, text_pos)

        # Draw focus glow if element is focused
        if self.focused:
            glow_rect = self.rect.inflate(6, 6)
            pygame.draw.rect(surface, focus_glow, glow_rect, 2)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle mouse clicks to toggle state, and keyboard activation via UIManager.

        Args:
            event (pygame.event.Event): The event to process.
        """
        # Toggle on left mouse button click within checkbox bounds
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self._toggle_state()

    def update(self, mouse_pos: tuple[int, int]) -> None:
        """
        Currently no hover behavior. Placeholder for future enhancements.

        Args:
            mouse_pos (tuple[int, int]): Cursor coordinates.
        """
        pass

    def activate(self) -> None:
        """
        Called by UIManager when ENTER/SPACE is pressed on this focused element.
        Toggles the checkbox state.
        """
        self._toggle_state()

    def _toggle_state(self) -> None:
        """
        Internal helper to invert the checked flag and invoke callback.
        """
        self.checked = not self.checked
        logger.debug("UICheckbox '%s' toggled to %s", self.label, self.checked)
        if self.callback:
            try:
                self.callback(self.checked)
            except Exception:
                logger.exception("Error in checkbox callback for '%s'", self.label)
