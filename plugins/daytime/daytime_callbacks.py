
import logging

logger = logging.getLogger(__name__)

def on_sleep_button_clicked(context):
    """
    Sets the current daytime phase to 'Morning' via the DaytimeCycle plugin API.
    """
    if hasattr(context, "set_day_phase"):
        logger.info("[SleepPlugin] Sleeping... setting time to Morning.")
        context.set_day_phase("Morning")
    else:
        logger.warning("[SleepPlugin] DaytimeCycle API not available.")

def make_daytime_changed_handler(label):
    """
    Returns a callback that updates the given UILabel when the time of day changes.
    """
    def handler(phase):
        label.set_text(f"Time: {phase}")
        logger.info(f"[TimeLabelPlugin] Updated label to: {phase}")
    return handler