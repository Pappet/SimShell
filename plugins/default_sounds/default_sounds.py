# plugins/default_sounds.py
import logging
import os
from core.events.event_types import EventType
from core.plugin import Plugin
from ui.components.button import Button

logger = logging.getLogger(__name__)

class PluginImpl(Plugin):
    def on_init(self):
        # load Sounds 
        self.app.context.sound_manager.load("start_click", os.path.join("assets","sounds","select_008.wav"))
        self.app.context.sound_manager.load("exit_click", os.path.join("assets","sounds","exit.wav"))
        self.app.context.sound_manager.load("default_click", os.path.join("assets","sounds","click_001.wav"))
        self.app.context.sound_manager.load("add_click", os.path.join("assets","sounds","maximize_009.wav"))
        self.app.context.sound_manager.load("sup_click", os.path.join("assets","sounds","minimize_009.wav"))

    def on_event(self, event):
        if isinstance(event, Button):
            try:
                sound_key = getattr(event, "sound_key", None) or "default_click"
                print(sound_key)
                self.app.context.sound_manager.play(sound_key)
            except Exception as e:
                logging.error(f"Error playing sound: {e}")