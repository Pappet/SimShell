# scenes/plugin_manager_scene.py
import pygame
import logging
import setup.config as Config 
from ui.components.label import Label
from ui.components.button import Button
from core.scene_registry import scene
from themes.theme_manager import get_color
from ui.ui_manager import UIManager

logger = logging.getLogger(__name__)

@scene("plugins")
class PluginManagerScene:
    def __init__(self, app):
        self.app = app
        self.pm  = app.plugin_manager
        # UIManager hält alle Buttons
        self.ui = UIManager()
        self._build_ui()

    def _build_ui(self):
        # 1) UIManager zurücksetzen
        self.ui.clear()  

        # 2) Zurück‑Button
        back_btn = Button(
            rect=pygame.Rect(300, 300, 200, 40),
            text="Zurück zum Menü",
            callback=lambda: self.app.scene_manager.switch_scene("menu")
        )
        self.ui.add(back_btn)

        # 3) Plugin‑Toggle‑Buttons
        y = 100
        for meta in self.pm.available:
            btn = Button(
                rect=pygame.Rect(400, y, 120, 30),
                text="Ein" if meta["enabled"] else "Aus",
                callback=lambda m=meta: self._toggle(m)
            )
            label = Label(text=meta["name"], position=(50, y))
            self.ui.add(label)
            self.ui.add(btn)
            y += 40

    def _toggle(self, meta):
        # Plugin aktivieren/deaktivieren
        if meta["enabled"]:
            self.pm.disable_plugin(meta["name"])
            meta["enabled"] = False
        else:
            self.pm.enable_plugin(meta["name"])
            meta["enabled"] = True
        # UI neu aufbauen, inklusive Back‑Button
        self._build_ui()

    def handle_event(self, event):
        self.ui.handle_event(event)

    def update(self):
        # UIManager muss wissen, wo die Maus steht & intern State updaten
        mouse_pos = pygame.mouse.get_pos()
        self.ui.update(mouse_pos)

    def draw(self, surface):
        surface.fill(get_color("background"))
        # Überschrift
        font = pygame.font.SysFont(
            Config.fonts["title"]["name"],
            Config.fonts["title"]["size"]
        )
        surface.blit(font.render("Plugins verwalten", True, get_color("foreground")), (50, 50))
        # UI zeichnen (alle Buttons)
        self.ui.draw(surface)
