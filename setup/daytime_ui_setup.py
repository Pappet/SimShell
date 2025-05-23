# setup/game_ui_setup.py (Teil eines return-Dicts)

from ui.components.label import UILabel
from ui.components.button import UIButton
from ui.layout.vertical import VerticalLayout
from core.events.event_types import EventType
from plugins.daytime.view import DaytimeLabel
from plugins.calendar.view import CalendarLabel
from ui.ui_manager import UIManager
from plugins.daytime.callbacks import on_sleep_button_clicked, make_daytime_changed_handler

def create_game_ui(stat_manager, event_manager, switch_scene_callback, context):
    ui = UIManager(event_manager)

    layout = VerticalLayout(
        x=200, y=100,
        spacing=10,
        align="center"
    )

    daytime_model = context.create_daytime()
    daytime_label = DaytimeLabel(daytime_model, x=0, y=0)

    cal_model = context.create_calendar()
    cal_label = CalendarLabel(cal_model, x=0, y=0)
    
    # Back button to return to the main menu
    back_button = UIButton(
        x=0, y=0,
        width=200, height=40,
        text="Zurück zum Menü",
        callback=lambda: switch_scene_callback("menu"),
        sound_key="exit_click"
    )

    layout.add(daytime_label)
    layout.add(cal_label)
    layout.add(back_button)
    
    # Register DAYTIME_CHANGED event listener
    handler = make_daytime_changed_handler(daytime_label)
    context.event_manager.register(EventType.DAYTIME_CHANGED, handler)

    for element in layout.get_elements():
        ui.add(element)

    return ui
