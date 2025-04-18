# core/app.py


'''
GameApp class for managing the game loop and initializing the game.
It handles the main game loop, event processing, and rendering.
It also initializes the game context and scene manager.
It is the entry point for the game application.
'''

import pygame
import sys
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FONT_NAME, DEBUG_FONT_SIZE
import utility.color as Color
from core.scene_manager import SceneManager
from core.context import GameContext
from core.debug_console import DebugConsole


class GameApp:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(FONT_NAME, DEBUG_FONT_SIZE)
        self.debug_console = DebugConsole(self.font)

        self.context = GameContext(self.debug_console)
        self.scene_manager = SceneManager(self.context, self.debug_console, app=self)
                
        self.running = True
        self.debug = False
        self.scene_manager.switch_scene("menu")

    def run(self):
        while self.running:
            self.screen.fill(Color.WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.exit_game()
                self.scene_manager.handle_event(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    self.debug = not self.debug
                    self.debug_console.log("Debug mode toggled.")
            
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
        self.debug_console.log("Exiting game.")
        print("Exiting game...")
        pygame.quit()
        sys.exit()
