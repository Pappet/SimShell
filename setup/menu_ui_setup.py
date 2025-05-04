# setup/menu_ui_setup.py

"""
Module for constructing the main menu UI.
"""

import core.events.callbacks as Callbacks
import setup.config as Config
from ui.components.button import UIButton
from ui.components.label import UILabel
from ui.ui_manager import UIManager
from ui.layout.vertical import VerticalLayout


def create_main_menu_ui(
    event_manager,
    switch_scene_callback: callable,
    exit_callback: callable
) -> UIManager:
    """
    Create and return the main menu UI manager with title and buttons.

    Args:
        switch_scene_callback (callable): Function to switch scenes.
        exit_callback (callable): Function to exit the application.

    Returns:
        UIManager: Configured UI manager for the main menu.
    """
    ui = UIManager()

    # Main vertical layout for menu items
    layout = VerticalLayout(x=300, y=100, spacing=10, align="center")

    # Title label
    title_label = UILabel(        
        x=0,
        y=0,
        text="Hauptmenü",
        font_size=Config.fonts["title"]["size"],
        font_name=Config.fonts["title"]["name"]
    )

    # Menu buttons
    start_button = UIButton(
        x=0, y=0,
        width=200, height=50,
        text="Spiel starten",
        callback=lambda: switch_scene_callback("game"),
        event_manager=event_manager,
        sound_key="start_click"
    )

    daytime_button = UIButton(
        x=0, y=0,
        width=200, height=50,
        text="Daytime starten",
        callback=lambda: switch_scene_callback("daytime"),
        event_manager=event_manager,
        sound_key="start_click"
    )

    theme_button = UIButton(
        x=0, y=0,
        width=200, height=50,
        text="Thema wechseln",
        callback=lambda: Callbacks.toggle_theme(),
        event_manager=event_manager
    )

    plugins_button = UIButton(
        x=0, y=0,
        width=200, height=50,
        text="Plugins Manager",
        callback=lambda: switch_scene_callback("plugins"),
        event_manager=event_manager
    )

    exit_button = UIButton(
        x=0, y=0,
        width=200, height=50,
        text="Beenden",
        callback=exit_callback,
        event_manager=event_manager,
        sound_key="exit_click"
    )

    # Add all elements to the layout
    layout.add(title_label)
    layout.add(start_button)
    layout.add(daytime_button)
    layout.add(theme_button)
    layout.add(plugins_button)
    layout.add(exit_button)

    # Register layout elements with UI manager
    for element in layout.get_elements():
        ui.add(element)

    return ui
