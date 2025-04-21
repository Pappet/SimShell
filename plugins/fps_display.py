# plugins/fps_display.py
import logging
import pygame
from core.plugin import Plugin

logger = logging.getLogger(__name__)

class PluginImpl(Plugin):
    def on_init(self):
        self.font = pygame.font.SysFont("Arial", 14)

    def on_render(self, surface):
        fps = int(self.app.clock.get_fps())
        text = self.font.render(f"FPS: {fps}", True, (0, 255, 0))
        surface.blit(text, (10, 10))

    def on_shutdown(self):
        pass
        
