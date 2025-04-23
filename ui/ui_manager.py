'''
UIManager class for managing UI elements.
It handles adding, updating, drawing, and removing UI elements.
It also handles events for UI elements.
''' 
import logging
from ui.components.base import UIElement

logger = logging.getLogger(__name__)

class UIManager:
    def __init__(self):
        # List of managed UI elements
        self.elements: list[UIElement] = []
        logger.debug("UIManager initialized.")

    def add(self, element):
        """Add a new UI element."""
        self.elements.append(element)
        
        logger.debug(f"Added element: {element}")

    def remove(self, element):
        """Remove a specific UI element if present."""
        try:
            self.elements.remove(element)
            logger.debug(f"Removed element: {element}")
        except ValueError:
            logger.warning(f"Attempted to remove non-existent element: {element}")

    def clear(self):
        """Remove all UI elements."""
        self.elements.clear()
        logger.debug("Cleared all UI elements.")

    def handle_event(self, event):
        """Dispatch the event to all UI elements."""       
        for element in list(self.elements):
            if hasattr(element, "handle_event"):
                try:
                    element.handle_event(event)
                except Exception as e:
                    logger.exception(f"Error in handle_event of {element}: {e}")

    def update(self, mouse_pos):
        """Update all UI elements with current mouse position."""
        for element in list(self.elements):
            if hasattr(element, "update"):
                try:
                    element.update(mouse_pos)
                except Exception as e:
                    logger.exception(f"Error in update of {element}: {e}")

    def draw(self, surface):
        """Draw all UI elements to the given surface."""
        for element in list(self.elements):
            if hasattr(element, "draw"):
                try:
                    element.draw(surface)
                except Exception as e:
                    logger.exception(f"Error in draw of {element}: {e}")
