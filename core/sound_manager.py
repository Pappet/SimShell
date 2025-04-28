# core/sound_manager.py

import pygame
import logging

logger = logging.getLogger(__name__)

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        logger.debug("SoundManager initialized.")


    def load(self, key: str, filepath: str):
        try:
            self.sounds[key] = pygame.mixer.Sound(filepath)
            logger.info(f"Loaded sound: {key} from {filepath}")
        except Exception as e:
            logger.error(f"Failed to load sound '{key}': {e}")


    def play(self, key: str):
        sound = self.sounds.get(key)
        if sound:
            sound.play()
            logger.debug("Played Sound: %s", sound)

