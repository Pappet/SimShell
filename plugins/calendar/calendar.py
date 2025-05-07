"""
Plugin: Calendar
Purpose: Tracks weekday and day number, and provides a UILabel-compatible UI component.
Exposes create_calendar() for use in scene setup.
"""

import logging
from core.plugin import Plugin
from .model import CalendarModel
from .view import CalendarLabel  # jetzt das neue, UILabel-basierte View-Element

logger = logging.getLogger(__name__)

class PluginImpl(Plugin):
    def on_init(self):
        self.model = CalendarModel(self.app.context)
        self.app.context.create_calendar = self.create_calendar
        self.app.context.get_day = self.model.get_day
        self.app.context.get_weekday = self.model.get_weekday

        logger.info("[CalendarPlugin] Registered calendar factory")

    def create_calendar(self):
        return self.model

    def on_start(self):
        return super().on_start()
    
    def on_render(self, screen):
        return super().on_render(screen)

    def on_update(self, dt):
        return super().on_update(dt)
    
    def on_event(self, event):
        return super().on_event(event)

    def on_shutdown(self):
        return super().on_shutdown()