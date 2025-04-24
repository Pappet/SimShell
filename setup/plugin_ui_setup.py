# setup/plugin_ui_setup.py

"""
Module for constructing the Plugin Manager UI using the Table component.
Table spans the full window width minus padding.
"""

import setup.config as Config
from ui.components.table import Table
from ui.components.button import Button
from ui.ui_manager import UIManager


def create_plugin_manager_ui(
    plugin_manager,
    toggle_callback: callable,
    switch_scene_callback: callable
) -> UIManager:
    """
    Create and return the UI for the plugin manager scene using a full-width Table
    listing plugins with inline toggle buttons.

    Args:
        plugin_manager: Provides .available list of plugin metadata.
        toggle_callback (callable): Called with plugin metadata to toggle enable/disable.
        switch_scene_callback (callable): Function to switch back to main menu.

    Returns:
        UIManager: Configured UI manager for plugin manager.
    """
    ui = UIManager()

        # Calculate full-width table with padding
    padding = Config.ui['default']['padding']
    screen_w = Config.screen['width']
    available_w = screen_w - padding * 2

    # Allocate more width to the name column, less to status and action
    name_w = int(available_w * 0.6)
    status_w = int(available_w * 0.2)
    action_w = available_w - name_w - status_w
    column_widths = [name_w, status_w, action_w]

    # Instantiate the Table
    table = Table(
        x=padding,
        y=80,
        column_widths=column_widths,
        row_height=30,
        headers=["Plugin", "Status", "Action"],
        font_size=Config.fonts['default']['size'],
        font_name=Config.fonts['default']['name']
    )

    # Populate table rows with data and inline toggle Button
    for meta in plugin_manager.available:
        status = "On" if meta['enabled'] else "Off"
        toggle_btn = Button(
            x=0, y=0,
            width=column_widths[2] - 10,
            height=table.row_height - 10,
            text="Toggle",
            callback=lambda m=meta: toggle_callback(m)
        )
        table.add_row([meta['name'], status, toggle_btn])

    ui.add(table)

    # Back button below the table
    back_y = table.y + table.height + padding
    back_button = Button(
        x=padding,
        y=back_y,
        width=200,
        height=40,
        text="Back to Menu",
        callback=lambda: switch_scene_callback("menu")
    )
    ui.add(back_button)

    return ui
