from core.events.event_types import EventType

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class CalendarModel:
    def __init__(self, context):
        self.context = context
        self.day = 1
        self.weekday_index = 0
        self.last_phase = context.get_day_phase()

        self.context.event_manager.register(
            EventType.DAYTIME_CHANGED,
            self._handle_daytime_changed
        )

    def _handle_daytime_changed(self, phase):
        print("Event")
        if self.last_phase == "Night" and phase == "Morning":
            print("CHANGE")
            self.day += 1
            self.weekday_index = (self.weekday_index + 1) % len(WEEKDAYS)
        self.last_phase = phase

    def get_day(self):
        return self.day

    def get_weekday(self):
        return WEEKDAYS[self.weekday_index]
