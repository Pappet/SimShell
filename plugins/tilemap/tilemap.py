"""
Plugin: TileMap
Purpose: Provides a simple 2D tilemap that can be rendered and manipulated.
Tiles are drawn as colored rectangles.
"""

import logging
import pygame
from core.plugin import Plugin

logger = logging.getLogger(__name__)

TILE_SIZE = 32
MAP_WIDTH = 10
MAP_HEIGHT = 8

# Simple color map: tile_value -> color
TILE_COLORS = {
    0: (34, 139, 34),     # Grass
    1: (30, 144, 255),    # Water
    2: (169, 169, 169),   # Stone
}

class PluginImpl(Plugin):
    def on_init(self):
        # Create tile grid: 2D list of integers
        self.tiles = [
            [0 for _ in range(MAP_WIDTH)]
            for _ in range(MAP_HEIGHT)
        ]

        # Register simple API
        self.app.context.get_tile = self.get_tile
        self.app.context.set_tile = self.set_tile

        logger.info("[TileMapPlugin] Initialized")

    def get_tile(self, x, y):
        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
            return self.tiles[y][x]
        return None

    def set_tile(self, x, y, value):
        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
            self.tiles[y][x] = value
            logger.debug(f"[TileMapPlugin] Tile at ({x}, {y}) set to {value}")

    def on_render(self, surface):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                color = TILE_COLORS.get(tile, (0, 0, 0))
                rect = pygame.Rect(
                    x * TILE_SIZE + 200, y * TILE_SIZE + 100,  # offset for position
                    TILE_SIZE - 2, TILE_SIZE - 2               # padding between tiles
                )
                pygame.draw.rect(surface, color, rect)

    def on_start(self):
        return super().on_start()
    
    def on_event(self, event):
        return super().on_event(event)
    
    def on_update(self,dt):
        return super().on_update(dt)

    def on_shutdown(self):
        return super().on_shutdown()