"""
Plugin: TileMap
Purpose: Provides a TileMapModel and a TileMapView for use in scene setup.
"""

import logging
from core.plugin import Plugin
from .model import TileMapModel
from .view import TileMapView

logger = logging.getLogger(__name__)

class PluginImpl(Plugin):
    def on_init(self):
        self.app.context.create_tilemap = self.create_tilemap
        logger.debug("[TileMapPlugin] Registered tilemap factory")

    def on_start(self):
        return super().on_start()
    
    def on_render(self, screen):
        return super().on_render(screen)
    
    def on_update(self, dt):
        return super().on_update(dt)
    
    def create_tilemap(self, width=10, height=8, pos=(0, 0)):
        model = TileMapModel(width, height)
        x, y = pos  # 🛠️ Hier entpacken
        view = TileMapView(model, x, y)
        logger.debug(f"[TileMapPlugin] Tilemap created - w {width} / h {height} - pos {pos}")
        return model, view
    
    def on_event(self, event):
        return super().on_event(event)

    def on_shutdown(self):
        return super().on_shutdown()
