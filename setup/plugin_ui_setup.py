# setup/plugin_ui_setup.py

"""
Module for constructing the Plugin Manager UI.
"""

import setup.config as Config
from ui.components.button import Button
from ui.components.label import Label
from ui.components.panel import Panel
from ui.ui_manager import UIManager
from ui.layout.vertical import VerticalLayout
from ui.layout.horizontal import HorizontalLayout


def create_plugin_manager_ui(
    plugin_manager,
    toggle_callback: callable,
    switch_scene_callback: callable
) -> UIManager:
    """
    Create and return the UI for the plugin manager scene.

    Args:
        plugin_manager: Object providing .available list and enable/disable methods.
        toggle_callback (callable): Function to call when toggling a plugin (receives plugin metadata).
        switch_scene_callback (callable): Function to switch back to main menu.

    Returns:
        UIManager: Configured UI manager for plugin manager.
    """
    ui = UIManager()

    # Main layout for plugin entries
    layout = VerticalLayout(x=50, y=50, spacing=15, align="left")

    # Title label
    title_label = Label(
        text="Plugin Manager",
        x=0, y=0,
        font_size=Config.fonts["title"]["size"],
        font_name=Config.fonts["title"]["name"]
    )
    layout.add(title_label)

    # Plugin entries
    for meta in plugin_manager.available:
        row = HorizontalLayout(x=0, y=0, spacing=20)
        name_label = Label(text=meta["name"], x=0, y=0)
        toggle_text = "On" if meta["enabled"] else "Off"
        toggle_button = Button(
            x=0, y=0,
            width=80, height=30,
            text=toggle_text,
            callback=lambda m=meta: toggle_callback(m)
        )
        row.add(name_label)
        row.add(toggle_button)
        layout.add(row)

    # Back button to return to main menu
    back_button = Button(
        x=0, y=0,
        width=200, height=40,
        text="Back to Menu",
        callback=lambda: switch_scene_callback("menu")
    )
    layout.add(back_button)

    # Register all layout elements with UIManager
    for element in layout.get_elements():
        ui.add(element)

    return ui
