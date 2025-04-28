"""
Module core/events/event_handlers.py

Defines event handler functions that respond to dispatched game events by
updating UI elements, such as stat bars and labels, to reflect changes
in game statistics.
"""


def update_stat_ui(
    new_value: float,
    stat_bar: object,
    stat_label: object,
    stat_name: str
) -> None:
    """
    Handle a stat change event by updating the corresponding UI components.

    This function is intended to be registered with the EventManager for
    stat change events (e.g., HEALTH_CHANGED, ENERGY_CHANGED). It updates
    a progress bar and text label to reflect the new statistic value.

    Args:
        new_value (float): The updated stat value.
        stat_bar (UIElement): UI component representing a stat bar;
            must support set_value(new_value: float).
        stat_label (UIElement): UI component for displaying text;
            must support set_text(text: str).
        stat_name (str): The key or name of the statistic, used for label text.
    """
    # Update the visual bar representation to the new value
    stat_bar.set_value(new_value)
    # Update the text label to show the stat name and integer value
    stat_label.set_text(f"{stat_name.capitalize()}: {int(new_value)}")
