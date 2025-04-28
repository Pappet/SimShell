"""
Module core/plugin.py

Defines the base Plugin abstract class for game extensions. Plugins can
hook into lifecycle events: initialization, start, per-frame updates,
and shutdown, as well as react to game events and rendering.
"""

from abc import ABC, abstractmethod


class Plugin(ABC):
    """
    Abstract base class for all game plugins.

    Provides empty hook methods for plugin lifecycle and event handling. Each
    plugin can override these methods to inject custom behavior at specific
    points in the game loop.
    """
    def __init__(self, app: object):
        """
        Initialize the plugin with a reference to the main application.

        Args:
            app (GameApp): The main application instance providing access
                           to shared context and services.
        """
        self.app = app

    @abstractmethod
    def on_init(self) -> None:
        """
        Called once after the plugin is loaded to perform any setup logic.
        """
        pass

    @abstractmethod
    def on_start(self) -> None:
        """
        Called when the game loop is about to start; use for initializing
        state that depends on game start.
        """
        pass

    @abstractmethod
    def on_event(self, event: object) -> None:
        """
        Called for each Pygame event; allows plugins to respond to user input
        or game events.

        Args:
            event (pygame.event.Event): The event object to handle.
        """
        pass

    @abstractmethod
    def on_update(self, dt: float) -> None:
        """
        Called each frame before rendering; use to update plugin state.

        Args:
            dt (float): Delta time in seconds since last update.
        """
        pass

    @abstractmethod
    def on_render(self, surface: object) -> None:
        """
        Called each frame after scene rendering; use to draw plugin-specific
        overlays or visuals.

        Args:
            surface (pygame.Surface): The surface to draw onto.
        """
        pass

    @abstractmethod
    def on_shutdown(self) -> None:
        """
        Called when the game is exiting; use to clean up resources and save
        state if necessary.
        """
        pass
