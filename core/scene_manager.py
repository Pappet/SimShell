# core/scene_manager.py

"""
SceneManager class to manage different scenes in the game.
It handles switching, instantiation, caching, updating, and drawing.
"""

import logging
from core.scene_registry import scene_registry

logger = logging.getLogger(__name__)

class SceneManager:
    """
    Manager for game scenes: handles instantiation, caching, and transitions.
    """
    def __init__(
        self,
        context,
        app
    ):
        """
        Initialize the SceneManager.

        Args:
            context: GameContext providing dependencies for scenes.
            app: GameApp instance for exit_game callback.
        """
        self.context = context
        self.app = app
        self.current_scene = None
        self.scene_cache = {}
        logger.debug("SceneManager initialized.")

    def switch_scene(
        self,
        key: str
    ):
        """
        Switch to the scene identified by key. Caches scenes on first use.

        Args:
            key (str): Scene registry key.
        """
        if key not in self.scene_cache:
            if key == "menu":
                from scenes.main_menu_scene import MainMenuScene
                scene = MainMenuScene(
                    context=self.context,
                    switch_scene_callback=self.switch_scene,
                    exit_callback=self.app.exit_game
                )
            else:
                SceneClass = scene_registry.get(key)
                if not SceneClass:
                    logger.warning(f"Scene '{key}' not found in registry.")
                    return
                scene = SceneClass(
                    context=self.context,
                    switch_scene_callback=self.switch_scene
                )
            self.scene_cache[key] = scene
        self._activate(self.scene_cache[key])

    def _activate(
        self,
        scene
    ):
        """
        Activate the given scene as current.

        Args:
            scene: Scene instance to activate.
        """
        self.current_scene = scene
        logger.debug(f"Switched to scene: {scene}")

    def handle_event(
        self,
        event
    ):
        """
        Forward input events to the current scene.

        Args:
            event: Pygame event to handle.
        """
        if self.current_scene:
            self.current_scene.handle_event(event)

    def update(
        self
    ):
        """
        Update the current scene.
        """
        if self.current_scene:
            self.current_scene.update()

    def draw(
        self,
        surface
    ):
        """
        Draw the current scene onto the given surface.

        Args:
            surface: Pygame surface to draw on.
        """
        if self.current_scene:
            self.current_scene.draw(surface)
