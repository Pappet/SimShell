# core/app.py


'''
GameApp class for managing the game loop and initializing the game.
It handles the main game loop, event processing, and rendering.
It also initializes the game context and scene manager.
It is the entry point for the game application.
'''

import pygame
import sys
import core.config as Config
import utility.color as Color
from core.scene_manager import SceneManager
from core.context import GameContext
import logging

logger = logging.getLogger(__name__)

class GameApp:
    def __init__(self, debug_console=None):
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption(Config.TITLE)
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(Config.FONT_NAME, Config.DEBUG_FONT_SIZE)
        self.debug_console = debug_console

        self.context = GameContext(self.debug_console)
        self.scene_manager = SceneManager(self.context, self.debug_console, app=self)
                
        self.running = True
        self.debug = False
        self.scene_manager.switch_scene("menu")

    def run(self):
        while self.running:
            self.screen.fill(Color.BACKGROUND)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.exit_game()
                self.scene_manager.handle_event(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    self.debug = not self.debug
                    logger.debug("Debug mode is now {}".format("on" if self.debug else "off"))
            
            self.scene_manager.update()
            self.scene_manager.draw(self.screen)
            
            if self.debug:
                self.debug_console.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(60)

        self.exit_game()

    def exit_game(self):
        # exit the loop and close the game
        self.running = False
        logger.debug("Exiting game...")
        pygame.quit()
        sys.exit()
