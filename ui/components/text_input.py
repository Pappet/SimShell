"""
Module ui/components/text_input.py

Defines UITextInput, a focusable text input field with placeholder, change and submit callbacks.
Supports keyboard focus, blinking cursor, focus glow, and safe callback invocation.
"""

import logging
import pygame
from typing import Callable, Optional, Tuple

import setup.config as Config
from themes.theme_manager import get_color
from ui.components.base import UIElement

logger = logging.getLogger(__name__)


class UITextInput(UIElement):
    """
    Text input field UI element with focus handling, placeholder text, and callbacks.

    Attributes:
        text (str): The current input string.
        placeholder (str): Text shown when input is empty and unfocused.
        on_change (Callable[[str], None] | None): Called when text changes.
        on_enter (Callable[[str], None] | None): Called when the user activates input (ENTER/SPACE).
        focusable (bool): Indicates this element can receive keyboard focus.
        focused (bool): Current focus state.
        cursor_visible (bool): Whether the text cursor is currently visible.
        cursor_timer (int): Last toggle timestamp for blink timing.
        cursor_interval (int): Blink interval in milliseconds.
        font (pygame.font.Font): Font used to render text.
    """
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str = "",
        placeholder: str = "",
        on_change: Optional[Callable[[str], None]] = None,
        on_enter: Optional[Callable[[str], None]] = None
    ) -> None:
        """
        Initialize a UITextInput field.

        Args:
            x (int): X-coordinate of the input field.
            y (int): Y-coordinate of the input field.
            width (int): Width of the input field in pixels.
            height (int): Height of the input field in pixels.
            text (str, optional): Initial text content. Defaults to empty.
            placeholder (str, optional): Placeholder text when empty and unfocused.
            on_change (Callable[[str], None], optional): Callback on text change.
            on_enter (Callable[[str], None], optional): Callback on activation.
        """
        super().__init__(x, y, width, height)
        self.text = text
        self.placeholder = placeholder
        self.on_change = on_change
        self.on_enter = on_enter

        # Enable keyboard focus behavior
        self.focusable = True
        self.focused = False

        # Cursor blink state
        self.cursor_visible = True
        self.cursor_timer = pygame.time.get_ticks()
        self.cursor_interval = 500  # ms

        # Text rendering font
        font_cfg = Config.fonts["default"]
        self.font = pygame.font.SysFont(font_cfg["name"], font_cfg["size"])

        logger.debug(
            "UITextInput initialized at (%d,%d) size (%d,%d)",
            x, y, width, height
        )

    def draw(self, surface: pygame.Surface) -> None:
        """
        Render the input field: background, border, focus glow, text or placeholder, and blinking cursor.

        Args:
            surface (pygame.Surface): Target surface to draw on.
        """
        # Retrieve theme colors
        bg_color = get_color("input_bg")
        border_color = get_color("border")
        text_color = get_color("input_text")
        placeholder_color = get_color("input_placeholder")
        cursor_color = get_color("input_cursor")
        focus_glow = get_color("focus_glow")

        # Draw background and border
        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(
            surface,
            border_color,
            self.rect,
            Config.ui["default"]["border_width"]
        )

        # Draw focus glow if focused
        if self.focused:
            glow_rect = self.rect.inflate(4, 4)
            pygame.draw.rect(surface, focus_glow, glow_rect, 2)

        # Determine content and color
        content = self.text if (self.text or self.focused) else self.placeholder
        color = text_color if (self.text or self.focused) else placeholder_color
        text_surf = self.font.render(content, True, color)
        text_pos = (
            self.x + 8,
            self.y + (self.height - text_surf.get_height()) // 2
        )
        surface.blit(text_surf, text_pos)

        # Draw blinking cursor when focused
        if self.focused and self.cursor_visible:
            cursor_x = self.x + 8 + self.font.size(self.text)[0]
            cursor_y = self.y + (self.height - self.font.get_height()) // 2
            cursor_h = self.font.get_height()
            pygame.draw.line(
                surface,
                cursor_color,
                (cursor_x, cursor_y),
                (cursor_x, cursor_y + cursor_h),
                2
            )

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle mouse and keyboard events for focus and text editing.

        - Mouse click toggles focus
        - Keyboard input edits text when focused (excluding ENTER, SPACE, TAB)
        - BACKSPACE deletes last character

        Args:
            event (pygame.event.Event): The event to process.
        """
        # Mouse click sets focus
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.focused = self.rect.collidepoint(event.pos)
            # Reset cursor blinking
            self.cursor_visible = True
            self.cursor_timer = pygame.time.get_ticks()
            logger.debug("UITextInput focus changed: %s", self.focused)

        # Keyboard input only when focused
        if self.focused and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                if self.on_change:
                    self._safe_call(self.on_change)
            elif event.key not in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_TAB):
                self.text += event.unicode
                if self.on_change:
                    self._safe_call(self.on_change)

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Update the cursor blink state based on time.

        Args:
            mouse_pos (Tuple[int, int]): Current mouse coordinates (unused).
        """
        now = pygame.time.get_ticks()
        if now - self.cursor_timer >= self.cursor_interval:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = now

    def activate(self) -> None:
        """
        Called by UIManager when ENTER or SPACE is pressed on this focusable element.
        Triggers the on_enter callback if provided.
        """
        if self.on_enter:
            self._safe_call(self.on_enter)

    def _safe_call(self, callback: Callable[[str], None]) -> None:
        """
        Invoke a callback with exception handling to avoid breaking the UI loop.

        Args:
            callback (Callable[[str], None]): The function to call with current text.
        """
        try:
            callback(self.text)
        except Exception:
            logger.exception("UITextInput callback error.")
