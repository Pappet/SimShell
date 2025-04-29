"""
Module main.py

Entry point for the SimShell game application. Configures global logging to both a rotating file and
an in-game debug console, initializes Pygame, and launches the GameApp loop.
"""

import logging
import pygame
from logging.handlers import RotatingFileHandler

import setup.config as Config
from core.debug_console import DebugConsole
from core.debug_console_handler import DebugConsoleHandler
from core.app import GameApp
from themes.theme_manager import get_color


def setup_logging(debug_console: DebugConsole) -> None:
    """
    Configure the application's logging framework with two handlers:

    1. RotatingFileHandler: logs all DEBUG+ messages to a file for persistent records.
       Controlled by Config.paths['log_file'], Config.logging['max_bytes'],
       and Config.logging['backup_count'].
    2. DebugConsoleHandler: routes INFO+ messages to the in-game DebugConsole
       for real-time feedback during gameplay.

    Args:
        debug_console (DebugConsole): The in-game console to display logs.
    """
    # Root logger setup
    root = logging.getLogger()
    root.setLevel(Config.logging['level'])  # Minimum level for processing

    # Clear existing handlers to avoid duplicate logging
    for handler in list(root.handlers):
        root.removeHandler(handler)

    # File handler for persistent logs
    file_handler = RotatingFileHandler(
        Config.paths['log_file'],
        maxBytes=Config.logging['max_bytes'],
        backupCount=Config.logging['backup_count']
    )
    file_handler.setLevel(Config.logging['file_level'])
    file_formatter = logging.Formatter(
        Config.logging['file_log_format'],
        datefmt=Config.logging['date_format']
    )
    file_handler.setFormatter(file_formatter)
    root.addHandler(file_handler)

    # In-game console handler for runtime feedback
    console_handler = DebugConsoleHandler(debug_console)
    console_handler.setLevel(Config.logging['console_level'])
    console_formatter = logging.Formatter(
        Config.logging['console_log_format']
    )
    console_handler.setFormatter(console_formatter)
    root.addHandler(console_handler)


if __name__ == '__main__':
    """
    Initialize Pygame, set up debug console and logging, then start the game loop.
    """
    # Initialize Pygame for fonts and mixer
    pygame.init()

    # Create font for debug console display
    font_cfg = Config.fonts['debug']
    font = pygame.font.SysFont(font_cfg['name'], font_cfg['size'])

    # Initialize in-game debug console with configured max lines
    debug_console = DebugConsole(
        font,
        max_lines=Config.ui['debug_console']['max_lines']
    )

    # Configure logging to file and debug console
    setup_logging(debug_console)
    
    # Launch the main game application with debug console enabled
    app = GameApp(debug_console=debug_console)
    app.run()