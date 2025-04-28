"""
Module core/sound_manager.py

Provides SoundManager for loading and playing audio assets using Pygame's mixer.
Handles initialization of the audio subsystem and simple sound playback.
"""

import logging
import pygame

logger = logging.getLogger(__name__)


class SoundManager:
    """
    Manages audio playback: initializes mixer, loads sound files, and plays them on demand.
    """

    def __init__(self) -> None:
        """
        Initialize the Pygame mixer subsystem and prepare the sound registry.
        """
        # Initialize audio mixer for playback
        pygame.mixer.init()
        # Dictionary mapping sound keys to Sound objects
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        logger.debug("SoundManager initialized.")

    def load(self, key: str, filepath: str) -> None:
        """
        Load a sound file into the manager under the given key.

        Args:
            key (str): Identifier for the loaded sound.
            filepath (str): Path to the audio file to load.
        """
        try:
            # Create Sound object and register it
            self.sounds[key] = pygame.mixer.Sound(filepath)
            logger.info("Loaded sound '%s' from '%s'", key, filepath)
        except Exception as e:
            # Log failure without interrupting game flow
            logger.error("Failed to load sound '%s' from '%s': %s", key, filepath, e)

    def play(self, key: str) -> None:
        """
        Play a previously loaded sound by key.

        Args:
            key (str): Identifier of the sound to play.
        """
        sound = self.sounds.get(key)
        if sound:
            # Trigger playback
            sound.play()
            logger.debug("Played sound: %s", key)
        else:
            # Warn if sound key is missing
            logger.warning("Sound '%s' not found. Cannot play.", key)
