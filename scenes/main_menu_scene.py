# scenes/main_menu_scene.py

import pygame
import utility.color as Color
from core.scene_registry import scene
from setup.menu_ui_setup import create_main_menu_ui

@scene("menu")
class MainMenuScene:
    def __init__(self, context, switch_scene_callback, exit_callback):
        self.context = context
        self.ui = create_main_menu_ui(switch_scene_callback, exit_callback, self.context.debug_console)
        self.context.debug_console.log("MainMenuScene initialized.")

    def handle_event(self, event):
        self.ui.handle_event(event)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.ui.update(mouse_pos)

    def draw(self, surface):
        surface.fill(Color.WHITE)
        self.ui.draw(surface)