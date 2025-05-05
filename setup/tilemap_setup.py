# setup/game_ui_setup.py (Teil eines return-Dicts)

from ui.components.label import UILabel
from ui.components.button import UIButton
from ui.layout.vertical import VerticalLayout
from core.events.event_types import EventType
from plugins.daytime.view import DaytimeLabel
from ui.ui_manager import UIManager
import setup.config as Config 
from plugins.daytime.callbacks import on_sleep_button_clicked, make_daytime_changed_handler

def create_game_ui(stat_manager, event_manager, switch_scene_callback, context):
    ui = UIManager(event_manager)

    layout = VerticalLayout(
        x=200, y=100,
        spacing=10,
        align="center"
    )

    # Title label
    title_label = UILabel(        
        x=0, y=0,
        text="TileMap Scene",
        font_size=Config.fonts["title"]["size"],
        font_name=Config.fonts["title"]["name"]
    )
    
    tile_map_model, map_view = context.create_tilemap(width=12, height=6, pos=(0, 0))

    # Back button to return to the main menu
    back_button = UIButton(
        x=0, y=0,
        width=200, height=40,
        text="Zurück zum Menü",
        callback=lambda: switch_scene_callback("menu"),
        sound_key="exit_click"
    )

    layout.add(title_label)
    layout.add(map_view)
    layout.add(back_button)
    
    for element in layout.get_elements():
        ui.add(element)

    return ui
