# ui/ui_manager.py

'''
UIManager class for managing UI elements.
It handles adding, updating, and drawing UI elements.
It also handles events for UI elements.
''' 

import logging


logger = logging.getLogger(__name__)

class UIManager:
    def __init__(self):
        self.elements = []
        logger.debug("UIManager initialized.")

    def add(self, element):
        self.elements.append(element)
        logger.debug(f"Added element: {element}")

    def handle_event(self, event):
        for element in self.elements:
            if hasattr(element, "handle_event"):
                element.handle_event(event)

    def update(self, mouse_pos):
        for element in self.elements:
            if hasattr(element, "update"):
                element.update(mouse_pos)

    def draw(self, surface):
        for element in self.elements:
            if hasattr(element, "draw"):
                element.draw(surface)