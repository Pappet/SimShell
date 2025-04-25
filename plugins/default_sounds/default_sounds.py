# plugins/default_sounds.py
import logging
import os
from core.events.event_types import EventType
from core.plugin import Plugin

logger = logging.getLogger(__name__)

class PluginImpl(Plugin):
    def on_init(self):
        # Sound laden
        self.app.context.sound_manager.load("click", os.path.join("assets","sounds","Click_Electronic_05.wav"))

    def on_event(self, event):
        # jedes UI-Button-Klick-Event abfangen
        if hasattr(event, "type") is False and event in (EventType.UI_BUTTON_CLICKED,):
            # wenn du das Event obj passt, besser:
            # if isinstance(event, UIEvent) und event.type==UI_BUTTON_CLICKED:
            self.app.context.sound_manager.play("click")