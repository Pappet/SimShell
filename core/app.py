"""
Module core/app.py

Defines the GameApp class, which initializes and runs the game loop,
handles event processing, manages scenes and plugins, and controls
rendering and shutdown procedures. Serves as the main entry point
for the application.
"""

import sys
import logging
import pygame
import os

from core.debug_console import DebugConsole
from core.debug_console_handler import DebugConsoleHandler
from core.events.event_types import EventType
import setup.config as Config
from core.plugin_manager import PluginManager
from core.scene_manager import SceneManager
from core.context import GameContext

logger = logging.getLogger(__name__)


class GameApp:
    """
    Main application class for the game.

    Responsibilities:
    - Initialize Pygame, window, clock, and core subsystems (plugins, context, scenes).
    - Run the main game loop: process events, update game state, render.
    - Manage debug console toggle and display.
    - Handle graceful shutdown of game and plugins.
    """
    def __init__(self, debug_console=None):
        """
        Create a new GameApp instance and set up all core components.

        Args:
            debug_console (DebugConsole, optional): External debug console instance.
                If None, one will be created using configured font settings.
        """
        # Control flags
        self.running = True     # Main loop flag
        self.debug = False      # Toggle for debug console display

        logger.debug("...Starting game...")

        # Initialize Pygame display and timing
        self.screen = pygame.display.set_mode(
            (Config.screen["width"], Config.screen["height"]))
        pygame.display.set_caption(Config.screen["title"])
        self.clock = pygame.time.Clock()

        # Store configuration and optional external console
        self.config = Config
        self.debug_console = debug_console

        # Initialize plugin manager and game context
        self.plugin_manager = PluginManager(app=self)
        self.context = GameContext(self.plugin_manager)

        # Initialize scene manager with context and application reference
        self.scene_manager = SceneManager(self.context, app=self)

        # Discover and initialize plugins
        self.plugin_manager.load_plugins()
        #self.plugin_manager.on_init()

        # Register UI button click events to plugin handler
        self.context.event_manager.register(
            EventType.UI_BUTTON_CLICKED,
            self.plugin_manager.on_event
        )

        # If no debug console provided, create one with configured font
        if debug_console is None:
            font_cfg = Config.fonts["debug"]
            font = pygame.font.SysFont(
                font_cfg["name"], font_cfg["size"]
            )
            self.debug_console = DebugConsole(
                font,
                max_lines=Config.ui["debug_console"]["max_lines"]
            )
            # Route standard logging output to in-game console
            logging.getLogger().addHandler(
                DebugConsoleHandler(self.debug_console)
            )

        # Switch to the initial scene defined in configuration
        self.scene_manager.switch_scene(
            Config.scenes["initial"]
        )

    def run(self):        
        """
        Enter the main game loop: handle events, update logic, render frames.
        Toggles debug console on pressing 'D', exits on window close or ESC.
        """
        # Notify plugins that the game is starting
        self.plugin_manager.on_start()

        # Main loop
        while self.running:
            # Delta time in seconds
            dt = self.clock.tick(Config.screen["fps"]) / 1000.0

            # Event handling
            for event in pygame.event.get():
                # Quit on window close
                if event.type == pygame.QUIT:
                    self.exit_game()

                # Toggle debug display on 'D' key
                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    self.debug = not self.debug
                    logger.debug(
                        "Debug mode is now %s",
                        "on" if self.debug else "off"
                    )

                # Forward event to current scene and plugins
                self.scene_manager.handle_event(event)
                self.plugin_manager.on_event(event)

            # Update logic for current scene and plugins
            self.scene_manager.update()
            self.plugin_manager.on_update(dt)

            # Render current scene and plugin overlays
            self.scene_manager.draw(self.screen)
            self.plugin_manager.on_render(self.screen)

            # Draw debug console overlay if enabled
            if self.debug:
                self.debug_console.draw(self.screen)

            # Flip display buffers
            pygame.display.flip()

    def exit_game(self):
        """
        Perform cleanup and exit the game: notify plugins, quit Pygame, and sys.exit().
        """
        # Stop main loop
        self.running = False

        # Notify plugins to perform shutdown operations
        self.plugin_manager.on_shutdown()
        logger.debug("...Exiting game...")
        logger.debug("------------------------------------------------------------------------------")

        # Clean up Pygame and exit process
        pygame.quit()
        sys.exit()
