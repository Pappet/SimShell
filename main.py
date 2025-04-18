import logging
import pygame
import core.config as Config
from core.debug_console import DebugConsole
from core.debug_console_handler import DebugConsoleHandler
from core.app import GameApp
import utility.color as Color
from logging.handlers import RotatingFileHandler

def setup_logging(debug_console: DebugConsole):
    # 2) Root‑Logger anlegen und Level setzen
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)  # niedrigstes Level, damit alle Handler ihre Level auswerten können

    # 3) Alle vorbestehenden Handler entfernen (z.B. basicConfig‑Handler)
    for h in root.handlers[:]:
        root.removeHandler(h)

    # 4) File‑Handler (DEBUG → simshell.log)
    file_handler = RotatingFileHandler("simshell.log", maxBytes=1_000_000, backupCount=3)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)-5s [%(name)s] %(message)s", datefmt="%H:%M:%S")
    )
    root.addHandler(file_handler)

    # 5) DebugConsole‑Handler (INFO → In‑Game‑Console)
    console_handler = DebugConsoleHandler(debug_console)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        logging.Formatter("%(levelname)-5s | %(message)s")
    )
    root.addHandler(console_handler)

if __name__ == "__main__":
    pygame.init()
    font = pygame.font.SysFont(Config.DEBUG_FONT_NAME, Config.DEBUG_FONT_SIZE)
    debug_console = DebugConsole(font, max_lines=10, color=Color.WHITE)
    
    setup_logging(debug_console)

    app = GameApp(debug_console=debug_console)  # GameApp speichert die Referenz
    app.run()