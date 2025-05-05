# setup/game_ui_setup.py (Teil eines return-Dicts)

from ui.components.label import UILabel
from ui.components.button import UIButton
from ui.layout.vertical import VerticalLayout
from core.events.event_types import EventType
from ui.ui_manager import UIManager
from plugins.daytime.callbacks import on_sleep_button_clicked, make_daytime_changed_handler

def create_game_ui(stat_manager, event_manager, switch_scene_callback, context):
    ui = UIManager(event_manager)

    layout = VerticalLayout(
        x=300, y=100
    )

    initial_phase = context.get_day_phase() if hasattr(context, "get_day_phase") else "(unknown)"

    # Label zur Anzeige der aktuellen Tageszeit
    time_label = UILabel(
        x=0, y=0, 
        text=f"Time: {initial_phase}"
    )

    sleep_button = UIButton(
        x=0, y=0, 
        width=200, height=100, 
        text="Sleep (Go to Morning)", 
        callback=lambda: on_sleep_button_clicked(context)
    )
    
    # Back button to return to the main menu
    back_button = UIButton(
        x=0, y=0,
        width=200, height=40,
        text="Zurück zum Menü",
        callback=lambda: switch_scene_callback("menu"),
        sound_key="exit_click"
    )

    model, view = context.create_tilemap(width=12, height=6, pos=(180, 120))
    

    layout.add(time_label)
    layout.add(sleep_button)
    layout.add(back_button)
    layout.add(view)
    # Register DAYTIME_CHANGED event listener
    handler = make_daytime_changed_handler(time_label)
    context.event_manager.register(EventType.DAYTIME_CHANGED, handler)

    

    for element in layout.get_elements():
        ui.add(element)

    return ui  # Wird als self.ui in GameScene verwendet
