# core/debug_console.py

"""
DebugConsole for in-game logging via Pygame.
Displays recent log messages with a semi-transparent background overlay.
"""

import pygame
import logging
from typing import List, Tuple
from themes.theme_manager import get_color
import setup.config as Config

logger = logging.getLogger(__name__)

class DebugConsole:
    """
    In-game debug console to display log messages on the screen.
    """
    def __init__(
        self,
        font: pygame.font.Font,
        max_lines: int = None
    ) -> None:
        """
        Initialize the DebugConsole.

        Args:
            font (pygame.font.Font): Font used to render text.
            max_lines (int, optional): Maximum number of lines to keep. 
                Defaults to Config.ui['debug_console']['max_lines'].
        """
        self.font = font
        self.logs: List[str] = []
        self.max_lines = (
            max_lines
            if max_lines is not None
            else Config.ui['debug_console']['max_lines']
        )
        self.color_key = 'foreground_console'

    def log(self, message: str) -> None:
        """
        Add a message with timestamp to the console.

        Args:
            message (str): The message to log.
        """
        timestamp = pygame.time.get_ticks() // 1000
        entry = f"{timestamp}: {message}"
        self.logs.append(entry)
        if len(self.logs) > self.max_lines:
            self.logs.pop(0)
        logger.debug("Console logged: %s", entry)

    def clear(self) -> None:
        """
        Clear all messages from the console.
        """
        self.logs.clear()

    def draw(
        self,
        surface: pygame.Surface,
        pos: Tuple[int, int] = (10, 10)
    ) -> None:
        """
        Draw the console background and messages.

        Args:
            surface (pygame.Surface): Surface to draw on.
            pos (tuple[int, int], optional): Top-left position. Defaults to (10,10).
        """
        # Refresh colors from theme
        fg_color = get_color(self.color_key)
        bg_color = get_color('background_console')

        x, y = pos
        line_height = self.font.get_linesize()
        padding = Config.ui['debug_console']['padding']

        # Compute background size
        max_text_width = 0
        for log in self.logs:
            width, _ = self.font.size(log)
            if width > max_text_width:
                max_text_width = width
        bg_width = max_text_width + padding * 2
        bg_height = line_height * len(self.logs) + padding * 2 + (len(self.logs) - 1) * 2

        # Draw semi-transparent background
        bg_surf = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        bg_surf.fill(bg_color)
        surface.blit(bg_surf, (x - padding, y - padding))

        # Draw log lines
        y_offset = y
        for log in self.logs:
            text_surf = self.font.render(log, True, fg_color)
            surface.blit(text_surf, (x, y_offset))
            y_offset += line_height + 2
