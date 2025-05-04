"""
Plugin: Calendar
Purpose: Tracks the number of passed days and the current weekday.
         Updates automatically when a new day begins (after Night → Morning).
         Displays this info via UILabels.
"""

import logging
from core.plugin import Plugin
from core.events.event_types import EventType
from ui.components.label import UILabel
from ui.ui_manager import UIManager
from .callbacks import make_daytime_change_handler

logger = logging.getLogger(__name__)

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class PluginImpl(Plugin):
    def on_init(self):
        self.day_count = 1
        self.weekday_index = 0
        self.ui = self.app.context.ui_manager

        # Labels
        self.label_day = UILabel(
            x=150, y=150,
            text=f"Day: {self.day_count}"
        )

        self.label_weekday = UILabel(
            x=150, y=200,
            text=f"Weekday: {WEEKDAYS[self.weekday_index]}"
        )

        self.ui.add(self.label_day)
        self.ui.add(self.label_weekday)

        # Create callback with local state
        handler = make_daytime_change_handler(
            context=self.app.context,
            label_day=self.label_day,
            label_weekday=self.label_weekday,
            get_day=lambda: self.day_count,
            set_day=lambda x: setattr(self, "day_count", x),
            get_index=lambda: self.weekday_index,
            set_index=lambda x: setattr(self, "weekday_index", x),
            weekdays=WEEKDAYS
        )
        self.app.context.event_manager.register(EventType.DAYTIME_CHANGED, handler)

        logger.info("[CalendarPlugin] Initialized")

    def on_start(self):
        return super().on_start()
    
    def on_event(self, event):
        return super().on_event(event)
    
    def on_update(self,dt):
        return super().on_update(dt)

    def on_render(self, surface):
        self.ui.draw(surface)

    def on_shutdown(self):
        return super().on_shutdown()
