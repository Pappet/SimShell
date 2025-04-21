# plugins/fps_display.py
import logging
import time
import pygame
from core.plugin import Plugin

logger = logging.getLogger(__name__)

class PluginImpl(Plugin):
    def on_init(self):
        self.font = pygame.font.SysFont("Arial", 14)

    def on_render(self, surface):
        current_time = time.strftime("%H:%M:%S", time.localtime())
        text = self.font.render(f"Uhrzeit: {current_time}", True, (0, 255, 0))
        surface.blit(text, (400, 10))

    def on_shutdown(self):
        print("shutdown")
        