# scenes/game_scene.py

"""
Scene for displaying the main game interface with stat controls.
"""

import pygame
import logging
from themes.theme_manager import get_color
from core.scene_registry import scene
from setup.game_ui_setup import create_game_ui

logger = logging.getLogger(__name__)

@scene("game")
class GameScene:
    """
    Scene class for the main gameplay screen, showing and updating stats.
    """
    def __init__(
        self,
        context,
        switch_scene_callback: callable
    ):
        """
        Initialize GameScene.

        Args:
            context: Game context providing stat_manager and event_manager.
            switch_scene_callback (callable): Function to switch scenes.
        """
        self.context = context
        self.switch_scene = switch_scene_callback
        # Build UI via setup module
        self.ui = create_game_ui(
            stat_manager=self.context.stat_manager,
            event_manager=self.context.event_manager,
            switch_scene_callback=self.switch_scene
        )
        logger.debug("GameScene initialized.")

    def handle_event(self, event: pygame.event.Event):
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

    def draw(self, surface: pygame.Surface):
        """
        Clear screen and render UI elements.
        """
        surface.fill(get_color("background"))
        self.ui.draw(surface)
