from ui.components.label import UILabel
from themes.theme_manager import get_color
from core.events.event_types import EventType

class CalendarLabel(UILabel):
    def __init__(self, model, x=0, y=0):
        self.model = model
        super().__init__(x, y, text=self._format_text())
        model.context.event_manager.register(EventType.DAYTIME_CHANGED, self._on_day_changed)

    def _format_text(self):
        return f"{self.model.get_weekday()} (Day {self.model.get_day()})"

    def _on_day_changed(self, phase):
        self.set_text(self._format_text())

