# callbacks.py – for CalendarPlugin
import logging

logger = logging.getLogger(__name__)

def make_daytime_change_handler(
    context,
    label_day,
    label_weekday,
    get_day,
    set_day,
    get_index,
    set_index,
    weekdays
):
    """
    Returns a callback that updates day count and weekday
    when phase changes from 'Night' to 'Morning'.
    """

    last_phase = context.get_day_phase() if hasattr(context, "get_day_phase") else None

    def handler(phase):
        nonlocal last_phase

        if last_phase == "Night" and phase == "Morning":
            # New day
            new_day = get_day() + 1
            new_index = (get_index() + 1) % len(weekdays)
            set_day(new_day)
            set_index(new_index)

            label_day.set_text(f"Day: {new_day}")
            label_weekday.set_text(f"Weekday: {weekdays[new_index]}")

            logger.info(f"[CalendarPlugin] New day: {new_day} ({weekdays[new_index]})")

        last_phase = phase

    return handler
