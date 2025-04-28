"""
Module scenes/plugin_manager_scene.py

Defines PluginManagerScene, responsible for displaying and managing game plugins.
Shows a list of available plugins with enable/disable toggles and handles
plugin lifecycle through UI interactions.
Registered in the scene_registry under the key "plugins".
"""

import pygame
import logging

from themes.theme_manager import get_color
from core.scene_registry import scene
from setup.plugin_ui_setup import create_plugin_manager_ui

logger = logging.getLogger(__name__)


@scene("plugins")
class PluginManagerScene:
    """
    Scene class for the plugin management interface.

    Responsibilities:
    - Display list of plugins with enable/disable controls
    - Handle user input to toggle plugin states
    - Refresh UI to reflect plugin state changes
    """
    def __init__(
        self,
        context: object,
        switch_scene_callback: callable
    ) -> None:
        """
        Initialize the plugin manager scene.

        Args:
            context: GameContext containing the PluginManager instance and EventManager.
            switch_scene_callback (callable): Function to call to change scenes.
        """
        self.context = context
        # Direct reference to the plugin manager for state changes
        self.pm = context.plugin_manager
        self.switch_scene = switch_scene_callback

        # Build UI elements via the plugin UI setup helper
        self.ui = create_plugin_manager_ui(
            self.pm,
            event_manager=self.context.event_manager,
            toggle_callback=self._toggle,
            switch_scene_callback=self.switch_scene
        )
        logger.debug("PluginManagerScene initialized with UI components.")

    def _toggle(self, meta: dict) -> None:
        """
        Enable or disable a plugin and rebuild the UI.

        Args:
            meta (dict): Metadata dict for the plugin (including 'name' and 'enabled').
        """
        if meta.get("enabled"):
            self.pm.disable_plugin(meta["name"])
            meta["enabled"] = False
        else:
            self.pm.enable_plugin(meta["name"])
            meta["enabled"] = True
        # Rebuild UI to reflect the updated plugin states
        self.ui = create_plugin_manager_ui(
            self.pm,
            event_manager=self.context.event_manager,
            toggle_callback=self._toggle,
            switch_scene_callback=self.switch_scene
        )
        logger.debug(
            "Plugin '%s' toggled, UI rebuilt.", meta.get("name")
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Forward Pygame events to the UI manager for processing.

        Args:
            event: The Pygame event to handle.
        """
        self.ui.handle_event(event)

    def update(self) -> None:
        """
        Update UI elements each frame with current mouse position.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.ui.update(mouse_pos)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Render the plugin manager scene: clear screen and draw UI elements.

        Args:
            surface: The Pygame Surface to draw onto.
        """
        surface.fill(get_color("background"))
        self.ui.draw(surface)