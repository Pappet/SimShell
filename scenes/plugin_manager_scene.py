# scenes/plugin_manager_scene.py

"""
Scene for managing plugins: list available plugins and toggle enable/disable.
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
    Scene class for displaying and toggling plugins.
    """
    def __init__(
        self,
        context,
        switch_scene_callback: callable
    ):
        """
        Initialize PluginManagerScene.

        Args:
            context: Game context containing plugin_manager.
            switch_scene_callback (callable): Function to switch scenes.
        """
        self.context = context
        # Assume plugin_manager attached to context
        self.pm = context.plugin_manager
        self.switch_scene = switch_scene_callback
        # Build UI manager via setup module
        self.ui = create_plugin_manager_ui(
            self.pm,
            toggle_callback=self._toggle,
            switch_scene_callback=self.switch_scene
        )

    def _toggle(self, meta):
        """
        Enable or disable a plugin and rebuild the UI.
        """
        if meta.get("enabled"):
            self.pm.disable_plugin(meta["name"])
            meta["enabled"] = False
        else:
            self.pm.enable_plugin(meta["name"])
            meta["enabled"] = True
        # Rebuild UI to reflect new states
        self.ui = create_plugin_manager_ui(
            self.pm,
            toggle_callback=self._toggle,
            switch_scene_callback=self.switch_scene
        )

    def handle_event(self, event):
        """
        Forward events to UI manager.
        """
        self.ui.handle_event(event)

    def update(self):
        """
        Update UI manager with current mouse position.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.ui.update(mouse_pos)

    def draw(self, surface):
        """
        Clear screen and draw UI elements with dynamic theme.
        """
        surface.fill(get_color("background"))
        self.ui.draw(surface)
