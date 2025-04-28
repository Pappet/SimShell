"""
Module ui/components/base.py

Defines the UIElement base class for all UI components.
Provides position, size, hit detection, and lifecycle hooks (draw, handle_event, update).
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
        # Rect for click and mouse-over detection
        self.rect = pygame.Rect(x, y, width, height)

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
        Called for each input event.

        Subclasses with click or input logic should override this method.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        pass

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Called once per frame with current mouse position.

        Use for hover effects or dynamic layout.

        Args:
            mouse_pos (tuple[int, int]): Current mouse coordinates.
        """
        pass

    def set_position(self, x: int, y: int) -> None:
        """
        Dynamically adjust the element's position.

        Updates both coordinates and the internal rect.

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
