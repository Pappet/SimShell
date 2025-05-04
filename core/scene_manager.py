"""
Module core/scene_manager.py

Defines SceneManager, responsible for handling scene lifecycle: discovery,
instantiation, caching, and transitions between game scenes.
"""

import logging
import inspect
import scenes
import pkgutil, importlib
for _, modname, _ in pkgutil.iter_modules(scenes.__path__): importlib.import_module(f"scenes.{modname}") 

from core.scene_registry import scene_registry

logger = logging.getLogger(__name__)


class SceneManager:
    """
    Manages game scenes by loading scene classes from the registry,
    caching instances, and facilitating scene transitions.
    """

    def __init__(self, context: object, app: object) -> None:
        """
        Initialize the SceneManager with shared context and application callback.

        Args:
            context: GameContext providing shared managers (event, stats, etc.).
            app: GameApp instance, used for providing exit_game callback when needed.
        """
        self.context = context
        self.app = app
        # Currently active scene instance
        self.current_scene = None
        # Cached scenes by registry key to avoid re-instantiation
        self.scene_cache: dict[str, object] = {}
        logger.debug("SceneManager initialized.")

    def switch_scene(self, key: str) -> None:
        """
        Switch to the scene identified by the given key, instantiating and caching it on first use.

        Uses the scene_registry to find a scene factory, inspects its constructor
        signature to determine required parameters (context, switch_scene_callback,
        optional exit_callback), then activates the new scene.

        Args:
            key (str): Registry key for the desired scene.
        """
        # Retrieve from cache if already created
        scene = self.scene_cache.get(key)
        if scene is None:
            # Lookup factory class for this scene key
            SceneFactory = scene_registry.get(key)
            if not SceneFactory:
                logger.warning(f"Scene '{key}' not found in registry.")
                return

            # Prepare constructor arguments
            kwargs = {
                'context': self.context,
                'switch_scene_callback': self.switch_scene,
            }
            # Inspect constructor to inject exit callback if required
            sig = inspect.signature(SceneFactory.__init__)
            if 'exit_callback' in sig.parameters:
                kwargs['exit_callback'] = self.app.exit_game

            # Instantiate the scene and cache it
            scene = SceneFactory(**kwargs)            
            self.scene_cache[key] = scene
            
        self.context.ui_manager = scene.ui
        print(self.context.ui_manager)
        # Activate the scene
        self._activate(scene)

    def _activate(self, scene: object) -> None:
        """
        Set the provided scene as the current active scene.

        Args:
            scene: The scene instance to activate.
        """
        self.current_scene = scene
        logger.debug(f"Switched to scene: {scene}")

    def handle_event(self, event: object) -> None:
        """
        Forward a Pygame event to the current scene for handling.

        Args:
            event: A pygame.event.Event instance representing user input or system events.
        """
        if self.current_scene:
            self.current_scene.handle_event(event)

    def update(self) -> None:
        """
        Update the logic of the current scene (called once per frame).
        """
        if self.current_scene:
            self.current_scene.update()

    def draw(self, surface: object) -> None:
        """
        Render the current scene onto the provided Pygame surface.

        Args:
            surface: pygame.Surface where the scene should draw its contents.
        """
        if self.current_scene:
            self.current_scene.draw(surface)
