# setup/game_ui_setup.py

from ui.components.button import Button
from ui.components.label import Label
from ui.components.panel import Panel
from ui.components.progressbar import ProgressBar
from ui.ui_manager import UIManager
from ui.layout.horizontal import HorizontalLayout
from ui.layout.vertical import VerticalLayout
import core.events.callbacks as Callbacks
import core.events.event_handlers as EventHandlers
from core.events.event_types import EventType
from themes.theme_manager import get_color
import core.config as Config

    
def create_game_ui(stat_manager, event_manager, switch_scene_callback):
    ui = UIManager()
    
    # Define keys for stats
    # These keys should match the keys used in the StatManager
    energy_key = "energy"
    health_key = "health"

    # Title Label
    title_Label = Label("Game Scene", (0, 0), Config.TITLE_FONT_SIZE, Config.TITLE_FONT_NAME)

    # Energy UI Elements
    energy_label = Label(f"{energy_key.capitalize()}: {stat_manager.get(energy_key)}", (0, 0))
    energy_bar = ProgressBar(0, 0, 200, 30, stat_manager.get(energy_key), stat_manager.get_max(energy_key), get_color("energy"))
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

    # Horizontal layout for energy buttons and bar
    row_energy = HorizontalLayout(x=0, y=0, spacing=15)
    row_energy.add(button_sub)
    row_energy.add(energy_bar)
    row_energy.add(button_add)

    # Panel für Energy
    energy_panel = Panel(x=10, y=10, width=340, height=100,
                         background_key='panel_bg',
                         border_key='border')
    panel_col_energy = VerticalLayout(x=0, y=0, spacing=15, align="center")
    panel_col_energy.add(energy_label)
    panel_col_energy.add(row_energy)
    energy_panel.add(panel_col_energy)

    # Health UI Elements
    health_label = Label(f"{health_key.capitalize()}: {stat_manager.get(health_key)}", (0, 0))
    health_bar = ProgressBar(0, 0, 200, 30, stat_manager.get(health_key), stat_manager.get_max(health_key), get_color("health"))
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

    # Horizontal layout for health buttons and bar
    row_health = HorizontalLayout(x=0, y=0, spacing=15)
    row_health.add(button_sub_health)
    row_health.add(health_bar)
    row_health.add(button_add_health)

    # Panel für Health
    health_panel = Panel(x=10, y=120, width=340, height=100,
                         background_key='panel_bg',
                         border_key='border')
    panel_col_health = VerticalLayout(x=0, y=0, spacing=15, align="center")
    panel_col_health.add(health_label)
    panel_col_health.add(row_health)
    health_panel.add(panel_col_health)

    # Back button to return to the main menu
    button_back = Button(
        (0, 0, 200, 40),
        "Zurück zum Menü",
        lambda: switch_scene_callback("menu")
    )

    # Creating the main layout
    # Vertical layout for the entire UI
    column = VerticalLayout(x=200, y=200, spacing=20, align="center")
    column.add(title_Label)
    column.add(energy_panel)
    column.add(health_panel)
    column.add(button_back)

    # Adding the Elements to the UI manager
    ui.add(title_Label)
    ui.add(energy_panel)
    ui.add(health_panel)
    ui.add(button_back)

    # Registering event handlers for energy and health changes
    event_manager.register(EventType.ENERGY_CHANGED, lambda new_value: EventHandlers.update_stat_ui(new_value, energy_bar, energy_label, energy_key))
    event_manager.register(EventType.HEALTH_CHANGED, lambda new_value: EventHandlers.update_stat_ui(new_value, health_bar, health_label, health_key))

    return ui