import logging
from core.events.event_types import EventType

logger = logging.getLogger(__name__)

DAY_PHASES = ["Morning", "Afternoon", "Evening", "Night"]

class DaytimeModel:
    def __init__(self, context):
        self.context = context
        self.current_phase_index = 0
        self.elapsed_time = 0
        self.change_interval = 2  # seconds
        self.last_phase = self.get_phase()

    def update(self, dt):
        self.elapsed_time += dt
        if self.elapsed_time >= self.change_interval:
            self.elapsed_time = 0
            self.advance()

    def advance(self):
        self.current_phase_index = (self.current_phase_index + 1) % len(DAY_PHASES)
        self._dispatch_phase_change()

    def set_phase(self, new_phase: str):
        if new_phase not in DAY_PHASES:
            logger.warning(f"[DaytimeModel] Unknown phase '{new_phase}'")
            return
        self.current_phase_index = DAY_PHASES.index(new_phase)
        self._dispatch_phase_change()

    def get_phase(self) -> str:
        return DAY_PHASES[self.current_phase_index]

    def _dispatch_phase_change(self):
        phase = self.get_phase()
        if phase != self.last_phase:
            logger.info(f"[DaytimeModel] New phase: {phase}")
            self.context.event_manager.dispatch(EventType.DAYTIME_CHANGED, phase=phase)
            self.last_phase = phase
