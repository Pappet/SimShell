# setup/game_ui_setup.py

from ui.components.button import Button
from ui.components.label import Label
from ui.components.progressbar import ProgressBar
from ui.ui_manager import UIManager
from ui.layout.horizontal import HorizontalLayout
from ui.layout.vertical import VerticalLayout
import core.events.callbacks as Callbacks
import core.events.event_handlers as EventHandlers
from core.events.event_types import EventType
import utility.color as Color


def create_game_ui(stat_manager, event_manager, switch_scene_callback, debug_console):
    ui = UIManager()
    
    energy_key = "energy"
    health_key = "health"

    #Energy UI Elements
    energy_label = Label(f"{energy_key.capitalize()}: {stat_manager.get(energy_key)}", (0, 0))
    energy_bar = ProgressBar(0, 0, 200, 30, stat_manager.get(energy_key), stat_manager.get_max(energy_key), Color.GREEN)
    button_add = Button(
        (0, 0, 100, 50),
        "+10",
        lambda: Callbacks.modify_stat(stat_manager, energy_key, 10)
    )
    button_sub = Button(
        (0, 0, 100, 50),
        "-10",
        lambda: Callbacks.modify_stat(stat_manager, energy_key, -10)
    )
    row_energy = HorizontalLayout(x=0, y=0, spacing=15, debug_console=debug_console)
    row_energy.add(button_sub)
    row_energy.add(energy_bar)
    row_energy.add(button_add)
    
    
    #Health UI Elements
    health_label = Label(f"{health_key.capitalize()} {stat_manager.get(health_key)}", (0, 0))
    health_bar = ProgressBar(0, 0, 200, 30, stat_manager.get(health_key), stat_manager.get_max(health_key), Color.RED)
    button_add_health = Button(
        (0, 0, 100, 50),
        "+10",
        lambda: Callbacks.modify_stat(stat_manager, health_key, 10)
    )
    button_sub_health = Button(
        (0, 0, 100, 50),
        "-10",
        lambda: Callbacks.modify_stat(stat_manager, health_key, -10)
    )

    button_back = Button(
        (0, 0, 200, 40),
        "Zurück zum Menü",
        lambda: switch_scene_callback("menu")
    )
    row_health = HorizontalLayout(x=0, y=0, spacing=15, debug_console=debug_console)
    row_health.add(button_sub_health)
    row_health.add(health_bar)
    row_health.add(button_add_health)

    # Creating the main layout
    # Vertical layout for the entire UI
    column = VerticalLayout(x=0, y=200, spacing=20, debug_console=debug_console)
    column.add(energy_label)
    column.add(row_energy)
    column.add(health_label)
    column.add(row_health)    
    column.add(button_back)

    # Registering event handlers for energy and health changes
    event_manager.register(EventType.ENERGY_CHANGED, lambda new_value: EventHandlers.update_stat_ui(new_value, energy_bar, energy_label, energy_key))
    event_manager.register(EventType.HEALTH_CHANGED, lambda new_value: EventHandlers.update_stat_ui(new_value, health_bar, health_label, health_key))

    # Adding the main layout to the UI manager
    for element in column.get_elements():
        ui.add(element)
    return ui