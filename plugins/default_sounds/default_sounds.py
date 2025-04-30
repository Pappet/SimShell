# plugins/default_sounds.py

import logging
import os
from core.plugin import Plugin
from ui.components.button import UIButton
from setup.config import sounds, paths


logger = logging.getLogger(__name__)

class PluginImpl(Plugin):
    def on_init(self):
        print("INIT")
        sounds_dir = paths.get('sounds_dir', os.path.join('assets', 'sounds'))

        for key, filename in sounds.items():
            full_path = os.path.join(sounds_dir, filename)
            try:
                self.app.context.sound_manager.load(key, full_path)
                logger.debug(f"Loaded sound {key} from {full_path}")
            except Exception as e:
                logger.error(f"Fehler beim Laden von Sound '{key}': {e}")

    def on_start(self):
        pass

    def on_event(self, event):
        if isinstance(event, UIButton):
            sound_key = getattr(event, "sound_key", None) or "default_click"
            try:
                self.app.context.sound_manager.play(sound_key)
            except Exception as e:
                logger.error(f"Error playing sound '{sound_key}': {e}")

    def on_update(self, dt):
        return super().on_update(dt)  

    def on_render(self, surface):
        return super().on_render(surface)

    def on_shutdown(self):
        return super().on_shutdown()
