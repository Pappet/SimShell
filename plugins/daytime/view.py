from ui.components.label import UILabel
from themes.theme_manager import get_color
from core.events.event_types import EventType

class DaytimeLabel(UILabel):
    def __init__(self, model, x=0, y=0):
        self.model = model
        super().__init__(x, y, text=f"Time: {model.get_phase()}")
        model.context.event_manager.register(EventType.DAYTIME_CHANGED, self._on_phase_changed)

    def _on_phase_changed(self, phase):
        self.set_text(f"Time: {phase}")
