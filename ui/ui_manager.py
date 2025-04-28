"""
Module core/ui_manager.py

Implements UIManager for managing UI elements throughout the application.
Handles adding, removing, event dispatching, updates, and rendering of UIElement instances.
"""

import logging
from ui.components.base import UIElement

logger = logging.getLogger(__name__)


class UIManager:
    """
    Central manager for UIElement instances.

    Responsibilities:
    - Maintain a list of active UI elements
    - Dispatch input events to elements
    - Update element states each frame
    - Draw elements onto the rendering surface
    """
    def __init__(self) -> None:
        """
        Initialize the UIManager with an empty element registry.
        """
        # List of managed UIElement instances
        self.elements: list[UIElement] = []
        logger.debug("UIManager initialized with no elements.")

    def add(self, element: UIElement) -> None:
        """
        Register a UI element for management.

        Args:
            element (UIElement): The UI component to add.
        """
        self.elements.append(element)
        logger.debug("Added UI element: %s", element)

    def remove(self, element: UIElement) -> None:
        """
        Unregister a UI element if it exists.

        Args:
            element (UIElement): The UI component to remove.
        """
        try:
            self.elements.remove(element)
            logger.debug("Removed UI element: %s", element)
        except ValueError:
            logger.warning("Attempted to remove non-existent UI element: %s", element)

    def clear(self) -> None:
        """
        Remove all UI elements from the manager.
        """
        self.elements.clear()
        logger.debug("Cleared all UI elements.")

    def handle_event(self, event: object) -> None:
        """
        Forward an input event to all UI elements that implement handle_event.

        Args:
            event: Event object (e.g., pygame.event.Event) to dispatch.
        """
        for element in list(self.elements):
            if hasattr(element, "handle_event"):
                try:
                    element.handle_event(event)
                except Exception as e:
                    logger.exception("Error in handle_event of %s: %s", element, e)

    def update(self, mouse_pos: tuple[int, int]) -> None:
        """
        Update UI element states, typically for hover effects.

        Args:
            mouse_pos (tuple[int, int]): Current mouse position coordinates.
        """
        for element in list(self.elements):
            if hasattr(element, "update"):
                try:
                    element.update(mouse_pos)
                except Exception as e:
                    logger.exception("Error in update of %s: %s", element, e)

    def draw(self, surface: object) -> None:
        """
        Draw all managed UI elements onto the specified surface.

        Args:
            surface: Rendering target (e.g., pygame.Surface).
        """
        for element in list(self.elements):
            if hasattr(element, "draw"):
                try:
                    element.draw(surface)
                except Exception as e:
                    logger.exception("Error in draw of %s: %s", element, e)
