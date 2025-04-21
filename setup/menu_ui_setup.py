# setup/menu_ui_setup.py

from ui.components.button import Button
from ui.components.label import Label
from ui.ui_manager import UIManager
from ui.layout.vertical import VerticalLayout
import core.events.callbacks as Callbacks
import setup.config as Config

def create_main_menu_ui(switch_scene_callback, exit_callback):
    ui = UIManager()

    layout = VerticalLayout(x=300, y=100, spacing=10, align="center")

    title_Label = Label("Hauptmenü", (0, 0), Config.fonts["title"]["size"], Config.fonts["title"]["name"])

    start_button = Button(
        (0, 0, 200, 50),
        "Spiel starten",
        lambda: switch_scene_callback("game")
    )

    theme_button = Button(
        (0, 0, 200, 50),
        "Thema wechseln",
        lambda: Callbacks.toggle_theme()
    )

    retro_button = Button(
        (0, 0, 200, 50),
        "Retro Thema wechseln",
        lambda: Callbacks.toggle_retro()
    )

    plugins_button = Button(
        (0, 0, 200, 50),
        "Plugins Manager",
        lambda: switch_scene_callback("plugins")
    )

    exit_button = Button(
        (0, 0, 200, 50),
        "Beenden",
        exit_callback 
    )

    layout.add(title_Label)
    layout.add(start_button)
    layout.add(theme_button)
    layout.add(retro_button)
    layout.add(plugins_button)
    layout.add(exit_button)
    

    for element in layout.get_elements():
        ui.add(element)

    return ui