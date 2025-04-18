# scenes/main_menu_scene.py

import pygame
import logging
from themes.theme_manager import get_color
from core.scene_registry import scene
from setup.game_ui_setup import create_game_ui

logger = logging.getLogger(__name__)

@scene("game")
class GameScene:
    def __init__(self, context, switch_scene_callback):
        self.context = context
        self.ui = create_game_ui(self.context.stat_manager, self.context.event_manager, switch_scene_callback)
        logger.debug("GameScene initialized.")

    def handle_event(self, event):
        self.ui.handle_event(event)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.ui.update(mouse_pos)

    def draw(self, surface):
        surface.fill(get_color("background"))
        self.ui.draw(surface)