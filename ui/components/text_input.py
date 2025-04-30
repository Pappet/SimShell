# ui/components/text_input.py

import pygame
import logging
from ui.components.base import UIElement
from themes.theme_manager import get_color
import setup.config as Config

logger = logging.getLogger(__name__)

class UITextInput(UIElement):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str = "",
        placeholder: str = "",
        on_change: callable = None,
        on_enter: callable = None
    ) -> None:
        super().__init__(x, y, width, height)
        self.text = text
        self.placeholder = placeholder
        self.on_change = on_change
        self.on_enter = on_enter
        self.focused = False

        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_interval = 500  # ms

        font_cfg = Config.fonts["default"]
        self.font = pygame.font.SysFont(font_cfg["name"], font_cfg["size"])

        logger.debug("UITextInput with cursor initialized at (%d,%d)", x, y)

    def draw(self, surface: pygame.Surface) -> None:
        bg_color = get_color("input_bg")
        border_color = get_color("border")
        text_color = get_color("input_text")
        placeholder_color = get_color("input_placeholder")
        cursor_color = get_color("input_cursor")

        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(surface, border_color, self.rect, Config.ui["default"]["border_width"])

        # Render text or placeholder
        content = self.text if self.text or self.focused else self.placeholder
        color = text_color if self.text or self.focused else placeholder_color
        text_surf = self.font.render(content, True, color)
        surface.blit(text_surf, (self.x + 8, self.y + (self.height - text_surf.get_height()) // 2))

        # Draw blinking cursor if focused
        if self.focused and self.cursor_visible:
            cursor_x = self.x + 8 + self.font.size(self.text)[0]
            cursor_y = self.y + (self.height - self.font.get_height()) // 2
            cursor_height = self.font.get_height()
            pygame.draw.line(surface, cursor_color, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.focused = self.rect.collidepoint(event.pos)
            self.cursor_timer = pygame.time.get_ticks()
            logger.debug(f"UITextInput focus changed: {self.focused}")

        if self.focused and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                if self.on_change:
                    self._safe_call(self.on_change)
            elif event.key == pygame.K_RETURN:
                if self.on_enter:
                    self._safe_call(self.on_enter)
            else:
                self.text += event.unicode
                if self.on_change:
                    self._safe_call(self.on_change)

    def update(self, mouse_pos: tuple[int, int]) -> None:
        # Cursor blink
        now = pygame.time.get_ticks()
        if now - self.cursor_timer >= self.cursor_interval:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = now

    def _safe_call(self, callback):
        try:
            callback(self.text)
        except Exception:
            logger.exception("UITextInput callback error.")
