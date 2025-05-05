import logging

logger = logging.getLogger(__name__)

class TileMapModel:
    def __init__(self, width=10, height=8, default=0):
        self.width = width
        self.height = height
        self.tiles = [
            [default for _ in range(width)]
            for _ in range(height)
        ]
        logger.info("[TileMapPlugin] Model Initialized")

    def get(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            #logger.info(f"[TileMapPlugin] Getting Tile {x}/{y} - {self.tiles[y][x]}")
            return self.tiles[y][x]
        logger.debug("[TileMapPlugin] Tile out of Bounds")
        return None

    def set(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            logger.info(f"[TileMapPlugin] Setting Tile {x}/{y} to {value}")
            self.tiles[y][x] = value
