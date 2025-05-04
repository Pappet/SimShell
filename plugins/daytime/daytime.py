"""
Plugin: DaytimeCycle
Purpose: Simulates a simple day-night cycle. Advances time every X seconds and dispatches a DAYTIME_CHANGED event.

States: ["Morning", "Afternoon", "Evening", "Night"]
"""

import logging
from core.plugin import Plugin
from core.events.event_types import EventType
import setup.config as Config
from themes.theme_manager import get_color
import pygame

logger = logging.getLogger(__name__)

DAY_PHASES = ["Morning", "Afternoon", "Evening", "Night"]
CHANGE_INTERVAL = 5  # seconds between phase changes

class PluginImpl(Plugin):
    def on_init(self):
        self.current_phase_index = 0
        self.elapsed_time = 0
        self.last_logged = -1
        self.phase = "Morning"
        logger.info("[DaytimeCycle] Initialized")
        self.app.context.get_day_phase = self.get_phase
        self.app.context.set_day_phase = self.set_phase

    def on_start(self):
        return super().on_start()

    def on_update(self, dt):
        self.elapsed_time += dt
        if self.elapsed_time >= CHANGE_INTERVAL:
            self.elapsed_time = 0
            self.current_phase_index = (self.current_phase_index + 1) % len(DAY_PHASES)
            self.phase = DAY_PHASES[self.current_phase_index]
            logger.info(f"[DaytimeCycle] Changed to: {self.get_phase()}")
            self.app.context.event_manager.dispatch(EventType.DAYTIME_CHANGED, phase=self.get_phase())
            self.app.context.daytime = self

    def get_phase(self):
        return self.phase
    
    def set_phase(self, new_phase: str):
        if new_phase not in DAY_PHASES:
            logger.warning(f"[DaytimeCycle] Unknown phase '{new_phase}', ignoring.")
            return

        if new_phase != self.get_phase():
            self.current_phase_index = DAY_PHASES.index(new_phase)
            self.phase = new_phase  # Optional, redundant – du könntest rein indexbasiert arbeiten
            self.app.context.event_manager.dispatch(
                EventType.DAYTIME_CHANGED,
                phase=new_phase
            )
            logger.info(f"[DaytimeCycle] Phase set to {new_phase}")


    def on_render(self, surface):
        return super().on_event(surface)
        # Optional: Draw current time phase as text on screen (top right corner)
        #font = pygame.font.SysFont(Config.fonts["default"]["name"], Config.fonts["default"]["size"])
        #text = font.render(f"Time: {self.get_phase()}", True, get_color("foreground"))
        #surface.blit(text, (surface.get_width() - 120, 10))

    def on_event(self, event):
        return super().on_event(event)

    def on_shutdown(self):
        return super().on_shutdown()