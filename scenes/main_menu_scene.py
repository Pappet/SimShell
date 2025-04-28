"""
Module scenes/main_menu_scene.py

Defines MainMenuScene, the initial menu interface for the game. Provides navigation
buttons for starting the game, opening plugin manager, and exiting.
Registered in the scene_registry under the key "menu".
"""

import pygame
import logging

from themes.theme_manager import get_color
from core.scene_registry import scene
from setup.menu_ui_setup import create_main_menu_ui

logger = logging.getLogger(__name__)


@scene("menu")
class MainMenuScene:
    """
    Scene class for displaying the main menu UI.

    Responsibilities:
    - Construct navigation UI elements (buttons) via setup helper
    - Handle user input to navigate to other scenes or exit
    - Render and update the menu interface each frame
    """
    def __init__(
        self,
        context: object,
        switch_scene_callback: callable,
        exit_callback: callable
    ) -> None:
        """
        Initialize the main menu scene.

        Args:
            context: GameContext for access to EventManager and other services.
            switch_scene_callback (callable): Function to call to change scenes.
            exit_callback (callable): Function to call to exit the application.
        """
        self.context = context
        self.switch_scene = switch_scene_callback
        self.exit = exit_callback

        # Build UI elements via the menu setup module
        self.ui = create_main_menu_ui(
            switch_scene_callback=self.switch_scene,
            exit_callback=self.exit,
            event_manager=self.context.event_manager
        )

        logger.debug("MainMenuScene initialized with UI components.")

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Forward Pygame events to the UI manager for processing button clicks.

        Args:
            event: The Pygame event to handle.
        """
        self.ui.handle_event(event)

    def update(self) -> None:
        """
        Update UI elements each frame with current input state.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.ui.update(mouse_pos)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Render the main menu: clear the screen and draw all UI components.

        Args:
            surface: The Pygame Surface to draw onto.
        """
        surface.fill(get_color("background"))
        self.ui.draw(surface)
