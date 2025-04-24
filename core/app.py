# core/app.py


'''
GameApp class for managing the game loop and initializing the game.
It handles the main game loop, event processing, and rendering.
It also initializes the game context and scene manager.
It is the entry point for the game application.
'''

import sys
import logging
import pygame
import setup.config as Config
from core.plugin_manager import PluginManager
from core.scene_manager import SceneManager
from core.context import GameContext


logger = logging.getLogger(__name__)

class GameApp:
    def __init__(self, debug_console=None):
        self.screen = pygame.display.set_mode((Config.screen["width"], Config.screen["height"]))
        pygame.display.set_caption(Config.screen["title"])
        self.clock = pygame.time.Clock()
        self.config = Config
        self.debug_console = debug_console

        self.plugin_manager = PluginManager(app=self)
        self.plugin_manager.load_plugins()

        self.context = GameContext(self.plugin_manager)
        self.scene_manager = SceneManager(self.context, app=self)
                
        self.running = True
        self.debug = False
        self.scene_manager.switch_scene(Config.scenes["initial"])


    def run(self):
        self.plugin_manager.on_init()
        self.plugin_manager.on_start()

        while self.running:
            dt = self.clock.tick(Config.screen["fps"]) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.exit_game()                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    self.debug = not self.debug
                    logger.debug("Debug mode is now {}".format("on" if self.debug else "off"))

                self.plugin_manager.on_event(event)
                self.scene_manager.handle_event(event)
            
            self.scene_manager.update()
            self.plugin_manager.on_update(dt)

            self.scene_manager.draw(self.screen)
            self.plugin_manager.on_render(self.screen)    
            if self.debug:
                self.debug_console.draw(self.screen)
            
            pygame.display.flip()
            

        self.exit_game()

    def exit_game(self):
        # exit the loop and close the game
        self.running = False
        self.plugin_manager.on_shutdown()
        logger.debug("Exiting game...")
        pygame.quit()
        sys.exit()
