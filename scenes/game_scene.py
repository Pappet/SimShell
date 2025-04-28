"""
Module scenes/game_scene.py

Defines GameScene, responsible for the main gameplay interface.
Handles UI initialization, input/event forwarding, per-frame updates, and rendering of stats.
Registered in the scene_registry under the key "game".
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
    Scene class for the primary game screen, displaying and updating player stats.

    Responsibilities:
    - Initialize UI components for stat bars and controls
    - Forward Pygame events to the UI manager
    - Perform per-frame UI updates based on input/state
    - Render background and UI elements
    """
    def __init__(
        self,
        context: object,
        switch_scene_callback: callable
    ) -> None:
        """
        Set up the GameScene with required dependencies.

        Args:
            context: GameContext providing stat_manager, event_manager, and other services.
            switch_scene_callback (callable): Function to invoke to change active scene.
        """
        self.context = context
        self.switch_scene = switch_scene_callback

        # Initialize UI elements via the setup helper module
        self.ui = create_game_ui(
            stat_manager=self.context.stat_manager,
            event_manager=self.context.event_manager,
            switch_scene_callback=self.switch_scene
        )
        logger.debug("GameScene initialized with UI components.")

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle incoming Pygame events by forwarding to the UI manager.

        Args:
            event (pygame.event.Event): The Pygame event to process.
        """
        self.ui.handle_event(event)

    def update(self) -> None:
        """
        Update UI state each frame, passing current mouse position.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.ui.update(mouse_pos)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Render the scene: clear the screen with background color and draw UI.

        Args:
            surface (pygame.Surface): The target surface for rendering.
        """
        # Fill background color from theme
        surface.fill(get_color("background"))
        # Draw UI elements on top
        self.ui.draw(surface)
