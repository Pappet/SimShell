# core/scenes/__init__.py

# jede neue Szene, die du anlegst, importierst du hier einmal:
from .main_menu_scene import MainMenuScene
from .game_scene import GameScene
# …usw.

# Optional: eine Liste für IDE‑Autovervollständigung
__all__ = ["MainMenuScene", "GameScene"]