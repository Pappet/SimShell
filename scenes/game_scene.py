# scenes/main_menu_scene.py

import pygame
import utility.color as Color
from core.scene_registry import scene
from setup.game_ui_setup import create_game_ui
import logging

logger = logging.getLogger(__name__)

@scene("game")
class GameScene:
    def __init__(self, context, switch_scene_callback):
        self.context = context
        self.ui = create_game_ui(self.context.stat_manager, self.context.event_manager, switch_scene_callback, self.context.debug_console)
        logger.debug("GameScene initialized.")

    def handle_event(self, event):
        self.ui.handle_event(event)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.ui.update(mouse_pos)

    def draw(self, surface):
        surface.fill(Color.BACKGROUND)
        self.ui.draw(surface)