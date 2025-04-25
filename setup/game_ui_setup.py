# setup/game_ui_setup.py

"""
Module for constructing the main game UI scene.
"""

import setup.config as Config
import core.events.callbacks as Callbacks
import core.events.event_handlers as EventHandlers
from core.events.event_types import EventType
from ui.components.button import Button
from ui.components.label import Label
from ui.components.panel import Panel
from ui.components.progressbar import ProgressBar
from ui.ui_manager import UIManager
from ui.layout.horizontal import HorizontalLayout
from ui.layout.vertical import VerticalLayout


def create_game_ui(
    stat_manager,
    event_manager,
    switch_scene_callback: callable
) -> UIManager:
    """
    Create and return the UI for the main game scene with stat bars and controls.

    Args:
        stat_manager: StatManager for retrieving and modifying stats.
        event_manager: EventManager for registering UI update callbacks.
        switch_scene_callback (callable): Function to switch scenes.

    Returns:
        UIManager: Configured UI manager for the game scene.
    """
    ui = UIManager()

    energy_key = "energy"
    health_key = "health"

    # Title label
    title_label = Label(
        text="Game Scene",
        x=0,
        y=0,
        font_size=Config.fonts["title"]["size"],
        font_name=Config.fonts["title"]["name"]
    )

    # Energy UI Elements
    energy_label = Label(
        text=f"{energy_key.capitalize()}: {stat_manager.get(energy_key)}",
        x=0,
        y=0
    )
    energy_bar = ProgressBar(
        x=0,
        y=0,
        width=200,
        height=30,
        current_value=stat_manager.get(energy_key),
        max_value=stat_manager.get_max(energy_key),
        color_key="energy"
    )
    energy_button_sub = Button(
        x=0, y=0,
        width=100, height=50,
        text="-10",
        callback=lambda: Callbacks.modify_stat(stat_manager, energy_key, -10),
        event_manager=event_manager
    )
    energy_button_add = Button(
        x=0, y=0,
        width=100, height=50,
        text="+10",
        callback=lambda: Callbacks.modify_stat(stat_manager, energy_key, 10),
        event_manager=event_manager
    )

    row_energy = HorizontalLayout(x=0, y=0, spacing=15)
    row_energy.add(energy_button_sub)
    row_energy.add(energy_bar)
    row_energy.add(energy_button_add)

    energy_panel = Panel(
        x=10, y=10,
        width=340, height=100,
        background_key="panel_bg",
        border_key="border"
    )
    panel_col_energy = VerticalLayout(x=0, y=0, spacing=15, align="center")
    panel_col_energy.add(energy_label)
    panel_col_energy.add(row_energy)
    energy_panel.add(panel_col_energy)

    # Health UI Elements
    health_label = Label(
        text=f"{health_key.capitalize()}: {stat_manager.get(health_key)}",
        x=0, y=0
    )
    health_bar = ProgressBar(
        x=0, y=0,
        width=200, height=30,
        current_value=stat_manager.get(health_key),
        max_value=stat_manager.get_max(health_key),
        color_key="health"
    )
    health_button_sub = Button(
        x=0, y=0,
        width=100, height=50,
        text="-10",
        callback=lambda: Callbacks.modify_stat(stat_manager, health_key, -10),
        event_manager=event_manager
    )
    health_button_add = Button(
        x=0, y=0,
        width=100, height=50,
        text="+10",
        callback=lambda: Callbacks.modify_stat(stat_manager, health_key, 10),
        event_manager=event_manager
    )

    row_health = HorizontalLayout(x=0, y=0, spacing=15)
    row_health.add(health_button_sub)
    row_health.add(health_bar)
    row_health.add(health_button_add)

    health_panel = Panel(
        x=10, y=120,
        width=340, height=100,
        background_key="panel_bg",
        border_key="border"
    )
    panel_col_health = VerticalLayout(x=0, y=0, spacing=15, align="center")
    panel_col_health.add(health_label)
    panel_col_health.add(row_health)
    health_panel.add(panel_col_health)

    # Back button to return to the main menu
    back_button = Button(
        x=0, y=0,
        width=200, height=40,
        text="Zurück zum Menü",
        callback=lambda: switch_scene_callback("menu"),
        event_manager=event_manager
    )

    # Main vertical layout for the scene
    main_layout = VerticalLayout(x=200, y=200, spacing=20, align="center")
    main_layout.add(title_label)
    main_layout.add(energy_panel)
    main_layout.add(health_panel)
    main_layout.add(back_button)

    for element in main_layout.get_elements():
        ui.add(element)

    # Register event handlers for dynamic stat updates
    event_manager.register(
        EventType.ENERGY_CHANGED,
        lambda new_value: EventHandlers.update_stat_ui(
            new_value, energy_bar, energy_label, energy_key
        )
    )
    event_manager.register(
        EventType.HEALTH_CHANGED,
        lambda new_value: EventHandlers.update_stat_ui(
            new_value, health_bar, health_label, health_key
        )
    )
    

    return ui
