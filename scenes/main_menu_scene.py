# scenes/main_menu_scene.py

import pygame
import logging
from themes.theme_manager import get_color
from core.scene_registry import scene
from setup.menu_ui_setup import create_main_menu_ui

logger = logging.getLogger(__name__)

@scene("menu")
class MainMenuScene:
    def __init__(self, context, switch_scene_callback, exit_callback):
        self.context = context
        self.ui = create_main_menu_ui(switch_scene_callback, exit_callback, self.context.debug_console)
        logger.debug("MainMenuScene initialized.")

    def handle_event(self, event):
        self.ui.handle_event(event)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.ui.update(mouse_pos)

    def draw(self, surface):
        surface.fill(get_color("background"))
        self.ui.draw(surface)