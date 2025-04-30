"""
Module ui/components/base.py

Defines the UIElement base class for all UI components.
Provides position, size, hit detection, keyboard focus handling, and lifecycle hooks.
"""

import pygame
from typing import Tuple


class UIElement:
    """
    Base class for UI components.

    Attributes:
        x (int): X-coordinate of the element's top-left corner.
        y (int): Y-coordinate of the element's top-left corner.
        width (int): Width of the element.
        height (int): Height of the element.
        rect (pygame.Rect): Rectangle used for hit detection and layout.
        focusable (bool): Whether the element can receive keyboard focus.
        focused (bool): Current keyboard focus state.
    """
    def __init__(self, x: int, y: int, width: int = 0, height: int = 0) -> None:
        """
        Initialize a UIElement with position and size.

        Args:
            x (int): Horizontal position in pixels.
            y (int): Vertical position in pixels.
            width (int, optional): Width in pixels. Defaults to 0.
            height (int, optional): Height in pixels. Defaults to 0.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.focusable = False
        self.focused = False
        # Rect for click and mouse-over detection
        self.rect = pygame.Rect(x, y, width, height)

    def set_focus(self, focused: bool) -> None:
        """
        Set or clear keyboard focus on this element.

        Args:
            focused (bool): True to give focus, False to remove.
        """
        self.focused = focused

    def activate(self) -> None:
        """
        Called when an activation key (ENTER/SPACE) is pressed while focused.
        Subclasses should override to perform actions (e.g., button click).
        """
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """
        Render the element onto the given surface.

        Must be implemented by subclasses.

        Args:
            surface (pygame.Surface): Target surface to draw on.
        """
        raise NotImplementedError("draw() must be implemented by UIElement subclasses")

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle an input event (mouse or keyboard).

        Subclasses with click or input logic should override this.

        Args:
            event (pygame.event.Event): The event to process.
        """
        pass

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Update element state each frame (e.g., hover visuals).

        Args:
            mouse_pos (tuple[int, int]): Current mouse coordinates.
        """
        pass

    def set_position(self, x: int, y: int) -> None:
        """
        Move the element to a new position.

        Args:
            x (int): New X-coordinate.
            y (int): New Y-coordinate.
        """
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

    def contains(self, point: Tuple[int, int]) -> bool:
        """
        Determine whether a point is inside the element's bounds.

        Args:
            point (tuple[int, int]): (x, y) coordinates to test.

        Returns:
            bool: True if the point lies within this element's rect.
        """
        return self.rect.collidepoint(point)
