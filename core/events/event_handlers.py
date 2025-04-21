'''
Event handlers for the game.
These functions are responsible for updating the UI elements in response to events.
They are called by the event manager when an event is dispatched.
'''


def update_stat_ui(new_value, stat_bar, stat_label, stat_name):
    stat_bar.set_value(new_value)
    stat_label.set_text(f"{stat_name.capitalize()}: {int(new_value)}") 