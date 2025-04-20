# scenes/plugin_manager_scene.py
import pygame
import logging
import setup.config as Config 
from ui.components.button import Button
from core.scene_registry import scene
from themes.theme_manager import get_color
from ui.ui_manager import UIManager


logger = logging.getLogger(__name__)

@scene("plugins")
class PluginManagerScene:
    def __init__(self, app):
        self.app = app
        self.pm = app.plugin_manager
        self.buttons = []  # List of (plugin_meta, toggle_button)
        self.ui = UIManager()
        self._build_ui()

    def _build_ui(self):
        self.buttons.clear()
        y = 100
        for meta in self.pm.available:
            name = meta["name"]
            enabled = meta["enabled"]
            btn = Button(
                rect=pygame.Rect(400, y, 120, 30),
                text="Ein" if enabled else "Aus",
                callback=lambda m=meta: self._toggle(m)
            )
            self.buttons.append((meta, btn))
            self.ui.add(btn)
            y += 40

    def _toggle(self, meta):
        if meta["enabled"]:
            self.pm.disable_plugin(meta["name"])
            meta["enabled"] = False
        else:
            self.pm.enable_plugin(meta["name"])
            meta["enabled"] = True
        # Button‑Text aktualisieren
        self._build_ui()

    def handle_event(self, event):
        for _, btn in self.buttons:
            btn.handle_event(event)

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(get_color("background"))
        # Überschrift
        font = pygame.font.SysFont(Config.fonts["title"]["name"], Config.fonts["title"]["size"])
        surface.blit(font.render("Plugins verwalten", True, (255,255,255)), (50, 50))
        # Liste mit Buttons
        for i, (meta, btn) in enumerate(self.buttons):
            surface.blit(
                font.render(meta["name"], True, (200,200,200)),
                (50, 100 + i*40)
            )
            btn.draw(surface)
