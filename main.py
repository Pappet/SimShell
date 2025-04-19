import logging
import pygame
import setup.config as Config
from core.debug_console import DebugConsole
from core.debug_console_handler import DebugConsoleHandler
from core.app import GameApp
from themes.theme_manager import get_color
from logging.handlers import RotatingFileHandler

def setup_logging(debug_console: DebugConsole):
    """
    Configures the application's logging system with two handlers:
    
    1. A rotating file handler that logs all DEBUG and higher messages to 'simshell.log'.
       This helps with persistent logging and debugging during development or after crashes.
    
    2. A custom debug console handler that logs INFO and higher messages to the in-game
       debug console for real-time feedback during gameplay.

    Parameters:
        debug_console (DebugConsole): The in-game console object that displays log messages.
    """

    # Configure the root logger to handle all log messages from the application
    root = logging.getLogger()
    root.setLevel(Config.logging["level"])  # Allow all messages to pass to the handlers

    # Remove any existing handlers (e.g., from basicConfig or previous setup)
    for h in root.handlers[:]:
        root.removeHandler(h)

    # Log all DEBUG and higher messages to a rotating file log
    file_handler = RotatingFileHandler(Config.paths["log_file"], maxBytes=Config.logging["max_bytes"], backupCount=Config.logging["backup_count"])
    file_handler.setLevel(Config.logging["file_level"])
    file_handler.setFormatter(
        logging.Formatter(Config.logging["file_log_format"], datefmt=Config.logging["date_format"])
    )
    root.addHandler(file_handler)

    # Log INFO and higher messages to the in-game debug console
    console_handler = DebugConsoleHandler(debug_console)
    console_handler.setLevel(Config.logging["console_level"])
    console_handler.setFormatter(
        logging.Formatter(Config.logging["console_log_format"])
    )
    root.addHandler(console_handler)

if __name__ == "__main__":
    # Initialize Pygame and create a debug console
    pygame.init()
    font = pygame.font.SysFont(Config.fonts["debug"]["name"], Config.fonts["debug"]["size"])
    debug_console = DebugConsole(font, max_lines=Config.ui["debug_console"]["max_lines"], color=get_color("foreground_console"))

    # Set up logging to file and debug console
    setup_logging(debug_console)

    # Create and run the game application
    app = GameApp(debug_console=debug_console)
    app.run()
