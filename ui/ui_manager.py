"""
Module ui/ui_manager.py

Implements UIManager for managing UI elements and focus navigation throughout the application.
Handles adding, removing, event dispatching, updates, rendering of UIElement instances,
and keyboard focus traversal among focusable elements.
"""

import logging
import pygame
from ui.components.base import UIElement

logger = logging.getLogger(__name__)


class UIManager:
    """
    Central manager for UIElement instances and keyboard focus.

    Responsibilities:
    - Maintain a list of active UI elements
    - Dispatch input events (mouse, keyboard) to elements
    - Navigate focus among focusable elements via Tab, arrows, and activation keys
    - Update element states each frame
    - Draw elements onto the rendering surface
    """
    def __init__(self, event_manager) -> None:
        """
        Initialize the UIManager with an empty element registry and no focus.
        """
        self.event_manager = event_manager
        self.elements: list[UIElement] = []
        # Index of currently focused element in focusable list, -1 if none
        self.focus_index = -1
        logger.debug("UIManager initialized with no elements.")

    def add(self, element: UIElement) -> None:
        """
        Register a UI element for management.

        Args:
            element (UIElement): The UI component to add.
        """
        if hasattr(element, "event_manager"):
            element.event_manager = self.event_manager
        self.elements.append(element)
        logger.debug("Added UI element: %s", element)

    def remove(self, element: UIElement) -> None:
        """
        Unregister a UI element if present.

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
        Remove all UI elements from the manager and clear focus.
        """
        self.elements.clear()
        self.clear_focus()
        logger.debug("Cleared all UI elements and focus.")

    def focus_next(self) -> None:
        """
        Move keyboard focus to the next focusable element.
        Cycles through elements with attribute `focusable = True`.
        """
        focusables = [e for e in self.elements if getattr(e, "focusable", False)]
        if not focusables:
            return
        # Unfocus current
        if 0 <= self.focus_index < len(focusables):
            focusables[self.focus_index].set_focus(False)
        # Advance index cyclically
        self.focus_index = (self.focus_index + 1) % len(focusables)
        focusables[self.focus_index].set_focus(True)

    def focus_prev(self) -> None:
        """
        Move keyboard focus to the previous focusable element.
        Cycles backwards through focusable elements.
        """
        focusables = [e for e in self.elements if getattr(e, "focusable", False)]
        if not focusables:
            return
        # Unfocus current
        if 0 <= self.focus_index < len(focusables):
            focusables[self.focus_index].set_focus(False)
        # Decrement index cyclically
        self.focus_index = (self.focus_index - 1) % len(focusables)
        focusables[self.focus_index].set_focus(True)

    def activate_focused(self) -> None:
        """
        Activate the currently focused element (e.g., invoke button press).
        """
        focusables = [e for e in self.elements if getattr(e, "focusable", False)]
        if 0 <= self.focus_index < len(focusables):
            focusables[self.focus_index].activate()

    def clear_focus(self) -> None:
        """
        Remove focus from any focused element and reset focus index.
        """
        focusables = [e for e in self.elements if getattr(e, "focusable", False)]
        if 0 <= self.focus_index < len(focusables):
            focusables[self.focus_index].set_focus(False)
        self.focus_index = -1

    def handle_event(self, event: object) -> None:
        """
        Forward an input event to UI elements and manage keyboard focus controls.

        - ESC clears focus
        - Tab/Shift+Tab and arrow keys navigate focus
        - Enter/Space activates focused element

        Args:
            event: Event object (e.g., pygame.event.Event) to dispatch.
        """
        # Keyboard focus navigation
        if hasattr(event, "type") and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.clear_focus()
                return
            if event.key == pygame.K_TAB:
                if event.mod & pygame.KMOD_SHIFT:
                    self.focus_prev()
                else:
                    self.focus_next()
                return
            if event.key == pygame.K_UP:
                self.focus_prev()
                return
            if event.key == pygame.K_DOWN:
                self.focus_next()
                return
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.activate_focused()
                return

        # Dispatch event to all elements
        for element in list(self.elements):
            if hasattr(element, "handle_event"):
                try:
                    element.handle_event(event)
                except Exception as e:
                    logger.exception("Error in handle_event of %s: %s", element, e)

    def update(self, mouse_pos: tuple[int, int]) -> None:
        """
        Update UI elements each frame, typically for hover and focus visuals.

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
