# plugins/fps_display.py
import logging
import pygame
from core.plugin import Plugin

logger = logging.getLogger(__name__)

class PluginImpl(Plugin):
    def on_init(self):
        self.font = pygame.font.SysFont("Arial", 14)

    def on_start(self):
        return super().on_start()

    def on_render(self, surface):
        fps = int(self.app.clock.get_fps())
        text = self.font.render(f"FPS: {fps}", True, (0, 255, 0))
        surface.blit(text, (10, 10))

    def on_event(self, event):
        return super().on_event(event)

    def on_update(self, dt):
        return super().on_update(dt)

    def on_shutdown(self):
        return super().on_shutdown()