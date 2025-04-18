# core/scene_manager.py

'''
SceneManager class to manage different scenes in the game.
It handles switching between scenes, updating them, and drawing them on the screen.
'''

import scenes
from core.scene_registry import scene_registry


class SceneManager:
    def __init__(self, context, debug_console, app):
        self.app = app
        self.debug_console = debug_console
        self.context = context
        self.current_scene = None
        self.scene_cache = {}

    def switch_scene(self, key):
        if key not in self.scene_cache:
            if key == "menu":
                from scenes.main_menu_scene import MainMenuScene
                scene = MainMenuScene(
                    self.context,
                    self.switch_scene,
                    self.app.exit_game
                )
            # alle anderen Scenes wie gehabt
            elif key in scene_registry:
                scene = scene_registry[key](self.context, self.switch_scene)
            else:
                self.debug_console.log(f"Scene for key: '{key}' not found.")
                return

            self.scene_cache[key] = scene
        self.switch_to(self.scene_cache[key])

    def switch_to(self, scene):
        if self.debug_console:
            self.debug_console.log(f"Switching to scene: {scene}")
        self.current_scene = scene

    def handle_event(self, event):
        if self.current_scene:
            self.current_scene.handle_event(event)

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def draw(self, surface):
        if self.current_scene:
            self.current_scene.draw(surface)