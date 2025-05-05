"""
Plugin: DaytimeCycle
Provides create_daytime() factory for use in scenes.
Handles automatic phase updates and event dispatching.
"""

import logging
from core.plugin import Plugin
from .model import DaytimeModel

logger = logging.getLogger(__name__)

class PluginImpl(Plugin):
    def on_init(self):
        self.model = DaytimeModel(self.app.context)
        self.app.context.create_daytime = self.create_daytime

        # Optional: globale Getter/Setter registrieren
        self.app.context.get_day_phase = self.model.get_phase
        self.app.context.set_day_phase = self.model.set_phase

        logger.info("[DaytimeCycle] Initialized")

    def on_start(self):
        return super().on_start()
    
    def on_render(self, screen):
        return super().on_render(screen)

    def on_update(self, dt):
        self.model.update(dt)

    def create_daytime(self):
        return self.model
    
    def on_event(self, event):
        return super().on_event(event)

    def on_shutdown(self):
        return super().on_shutdown()