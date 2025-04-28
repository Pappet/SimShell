"""
Module core/debug_console.py

Provides the DebugConsole class for on-screen, real-time logging in-game.
Displays recent log entries over a semi-transparent background, fetching
theme-based colors and respecting configured line limits.
"""

import logging
import pygame
from typing import List, Tuple

from themes.theme_manager import get_color
import setup.config as Config

logger = logging.getLogger(__name__)


class DebugConsole:
    """
    In-game debug console overlay for rendering log messages.

    Attributes:
        font (pygame.font.Font): Font used to render text lines.
        logs (List[str]): Stored log entries (with timestamps).
        max_lines (int): Maximum number of log lines to retain.
        color_key (str): Theme key for text color lookup.
    """
    def __init__(
        self,
        font: pygame.font.Font,
        max_lines: int = None
    ) -> None:
        """
        Initialize the DebugConsole instance.

        Args:
            font (pygame.font.Font): Pre-configured font for text rendering.
            max_lines (int, optional): Cap for stored log lines. If None,
                default from Config.ui['debug_console']['max_lines'] is used.
        """
        self.font = font
        # Internal storage of log entries
        self.logs: List[str] = []
        # Determine maximum number of lines
        self.max_lines = (
            max_lines
            if max_lines is not None
            else Config.ui['debug_console']['max_lines']
        )
        # Theme key for console text color
        self.color_key = 'foreground_console'

    def log(self, message: str) -> None:
        """
        Append a new log entry with a timestamp.

        Prepends the current runtime seconds to message, adds it to logs,
        and enforces the max_lines limit by dropping oldest entries.

        Args:
            message (str): The message to record.
        """
        # Compute seconds since game start
        timestamp = pygame.time.get_ticks() // 1000
        entry = f"{timestamp}: {message}"
        self.logs.append(entry)
        # Remove oldest line if exceeding capacity
        if len(self.logs) > self.max_lines:
            self.logs.pop(0)
        logger.debug("Console logged entry: %s", entry)

    def clear(self) -> None:
        """
        Remove all stored log entries.
        """
        self.logs.clear()
        logger.debug("DebugConsole cleared all log entries.")

    def draw(
        self,
        surface: pygame.Surface,
        pos: Tuple[int, int] = (10, 10)
    ) -> None:
        """
        Render the semi-transparent background and log entries onto the surface.

        Args:
            surface (pygame.Surface): Target drawing surface (game window).
            pos (Tuple[int,int], optional): Top-left origin for console. Defaults to (10,10).
        """
        # Fetch theming colors for text and background
        fg_color = get_color(self.color_key)
        bg_color = get_color('background_console')

        x, y = pos
        # Calculate line height and padding
        line_height = self.font.get_linesize()
        padding = Config.ui['debug_console']['padding']

        # Determine the widest log string for background width
        max_text_width = 0
        for log_entry in self.logs:
            width, _ = self.font.size(log_entry)
            if width > max_text_width:
                max_text_width = width
        bg_width = max_text_width + padding * 2
        # Total height: lines * line height + gaps + padding
        bg_height = (
            line_height * len(self.logs)
            + (len(self.logs) - 1) * 2  # spacing between lines
            + padding * 2
        )

        # Create an alpha-enabled surface for the background
        bg_surf = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        bg_surf.fill(bg_color)
        # Blit the semi-transparent rectangle
        surface.blit(bg_surf, (x - padding, y - padding))

        # Render each log line onto the main surface
        y_offset = y
        for log_entry in self.logs:
            text_surf = self.font.render(log_entry, True, fg_color)
            surface.blit(text_surf, (x, y_offset))
            # Advance y position for next line
            y_offset += line_height + 2
