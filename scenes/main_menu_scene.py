# scenes/main_menu_scene.py

"""
Scene for displaying the main menu with navigation buttons.
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
    Scene class for the main menu.
    """
    def __init__(
        self,
        context,
        switch_scene_callback: callable,
        exit_callback: callable
    ):
        """
        Initialize MainMenuScene.

        Args:
            context: Game context containing state and dependencies.
            switch_scene_callback (callable): Function to switch between scenes.
            exit_callback (callable): Function to exit the application.
        """
        self.context = context
        self.switch_scene = switch_scene_callback
        self.exit = exit_callback

        # Build UI using setup module
        self.ui = create_main_menu_ui(
            switch_scene_callback=self.switch_scene,
            exit_callback=self.exit
        )

        logger.debug("MainMenuScene initialized.")

    def handle_event(self, event):
        """
        Forward input events to the UI manager.
        """
        self.ui.handle_event(event)

    def update(self):
        """
        Update UI manager with current mouse position.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.ui.update(mouse_pos)

    def draw(self, surface):
        """
        Clear screen and render all UI elements.
        """
        surface.fill(get_color("background"))
        self.ui.draw(surface)
