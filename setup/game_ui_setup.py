# setup/game_ui_setup.py

"""
Module for constructing the main game UI scene.
"""

import setup.config as Config
import core.events.callbacks as Callbacks
import core.events.event_handlers as EventHandlers
from core.events.event_types import EventType
from ui.components.button import UIButton
from ui.components.label import UILabel
from ui.components.panel import UIPanel
from ui.components.checkbox import UICheckbox
from ui.components.progressbar import UIProgressBar
from ui.ui_manager import UIManager
from ui.layout.horizontal import HorizontalLayout
from ui.layout.vertical import VerticalLayout
from ui.components.text_input import UITextInput


def create_game_ui(
    stat_manager,
    event_manager,
    switch_scene_callback: callable,
    context
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
    title_label = UILabel(
        text="Game Scene",
        x=0,
        y=0,
        font_size=Config.fonts["title"]["size"],
        font_name=Config.fonts["title"]["name"]
    )

    # Energy UI Elements
    energy_label = UILabel(
        text=f"{energy_key.capitalize()}: {stat_manager.get(energy_key)}",
        x=0,
        y=0
    )
    energy_bar = UIProgressBar(
        x=0,
        y=0,
        width=200,
        height=30,
        current_value=stat_manager.get(energy_key),
        max_value=stat_manager.get_max(energy_key),
        color_key="energy"
    )
    energy_button_sub = UIButton(
        x=0, y=0,
        width=100, height=50,
        text="-10",
        callback=lambda: Callbacks.modify_stat(stat_manager, energy_key, -10),
        event_manager=event_manager,
        sound_key="sup_click"
    )
    energy_button_add = UIButton(
        x=0, y=0,
        width=100, height=50,
        text="+10",
        callback=lambda: Callbacks.modify_stat(stat_manager, energy_key, 10),
        event_manager=event_manager,
        sound_key="add_click"
    )

    row_energy = HorizontalLayout(x=0, y=0, spacing=15)
    row_energy.add(energy_button_sub)
    row_energy.add(energy_bar)
    row_energy.add(energy_button_add)

    energy_panel = UIPanel(
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
    health_label = UILabel(
        text=f"{health_key.capitalize()}: {stat_manager.get(health_key)}",
        x=0, y=0
    )
    health_bar = UIProgressBar(
        x=0, y=0,
        width=200, height=30,
        current_value=stat_manager.get(health_key),
        max_value=stat_manager.get_max(health_key),
        color_key="health"
    )
    health_button_sub = UIButton(
        x=0, y=0,
        width=100, height=50,
        text="-10",
        callback=lambda: Callbacks.modify_stat(stat_manager, health_key, -10),
        event_manager=event_manager,
        sound_key="sup_click"
    )
    health_button_add = UIButton(
        x=0, y=0,
        width=100, height=50,
        text="+10",
        callback=lambda: Callbacks.modify_stat(stat_manager, health_key, 10),
        event_manager=event_manager,
        sound_key="add_click"
    )

    row_health = HorizontalLayout(x=0, y=0, spacing=15)
    row_health.add(health_button_sub)
    row_health.add(health_bar)
    row_health.add(health_button_add)

    health_panel = UIPanel(
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
    back_button = UIButton(
        x=0, y=0,
        width=200, height=40,
        text="Zurück zum Menü",
        callback=lambda: switch_scene_callback("menu"),
        event_manager=event_manager,
        sound_key="exit_click"
    )

    text_label = UILabel("test", 0,0,)


    checkbox = UICheckbox(
        x=50,
        y=300,
        label="Enable Music",
        checked=True,
        callback=Callbacks.on_toggle
    )

    input_box = UITextInput(
        x=50, y=400,
        width=300, height=30,
        placeholder="Name eingeben...",
        on_enter=lambda new_text: Callbacks.update_label_text(text_label, new_text)
    )

    veri = VerticalLayout(50, 100, 20, "center")

    hori = HorizontalLayout(x=0, y=0, spacing=20, align="center")
    
    
    # Main vertical layout for the scene
    main_layout = VerticalLayout(x=0, y=0, spacing=20, align="left")    
    main_layout.add(input_box)
    main_layout.add(text_label)
    main_layout.add(checkbox)   

    second_layout = VerticalLayout(x=0, y=0, spacing=20, align="right")
    second_layout.add(energy_panel)
    second_layout.add(health_panel)

    hori.add(main_layout)
    hori.add(second_layout)

    veri.add(title_label)
    veri.add(hori)
    veri.add(back_button)

    for element in veri.get_elements():
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
