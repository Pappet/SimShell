import pygame
from ui.components.base import UIElement
import logging

logger = logging.getLogger(__name__)

TILE_SIZE = 32
TILE_COLORS = {
    0: (34, 139, 34),    # Grass
    1: (30, 144, 255),   # Water
    2: (169, 169, 169),  # Stone
}

class TileMapView(UIElement):
    def __init__(self, model, x=0, y=0):
        width = model.width * TILE_SIZE
        height = model.height * TILE_SIZE
        super().__init__(x, y, width, height)

        self.model = model
        logger.info("[TileMapPlugin] TileMap View Initialized")
        

    def draw(self, surface):
        for y in range(self.model.height):
            for x in range(self.model.width):
                value = self.model.get(x, y)
                color = TILE_COLORS.get(value, (0, 0, 0))
                rect = pygame.Rect(
                    self.x + x * TILE_SIZE,
                    self.y + y * TILE_SIZE,
                    TILE_SIZE - 2,
                    TILE_SIZE - 2
                )
                pygame.draw.rect(surface, color, rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if not self.contains((mx, my)):
                return

            grid_x = (mx - self.x) // TILE_SIZE
            grid_y = (my - self.y) // TILE_SIZE

            current = self.model.get(grid_x, grid_y)
            new_value = (current + 1) % len(TILE_COLORS)
            self.model.set(grid_x, grid_y, new_value)
