# setup/menu_ui_setup.py

from ui.components.button import Button
from ui.ui_manager import UIManager
from ui.layout.vertical import VerticalLayout

def create_main_menu_ui(switch_scene_callback, exit_callback, debug_console):
    ui = UIManager()

    layout = VerticalLayout(x=300, y=200, spacing=50, debug_console=debug_console)

    start_button = Button(
        (0, 0, 200, 50),
        "Spiel starten",
        lambda: switch_scene_callback("game")
    )

    exit_button = Button(
        (0, 0, 200, 50),
        "Beenden",
        exit_callback 
    )

    layout.add(start_button)
    layout.add(exit_button)

    for element in layout.get_elements():
        ui.add(element)

    return ui