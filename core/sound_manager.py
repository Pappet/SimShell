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
        """Lädt eine Sound-Datei unter dem angegebenen Schlüssel."""
        self.sounds[key] = pygame.mixer.Sound(filepath)
        logger.debug("Loaded Sound: %s", self.sounds[key])


    def play(self, key: str):
        """Spielt den Sound zum Schlüssel, falls vorhanden."""
        sound = self.sounds.get(key)
        if sound:
            sound.play()
            logger.debug("Played Sound: %s", sound)

