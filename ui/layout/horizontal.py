"""
Module ui/layouts/horizontal_layout.py

Defines HorizontalLayout for arranging UIElements in a horizontal row with spacing.
Automatically positions added elements, recalculates container bounds, and
propagates layout changes when moved.
"""

import pygame
from typing import List, Any, Tuple

from ui.components.base import UIElement


class HorizontalLayout:
    """
    Layout manager that arranges UI elements side by side.

    Attributes:
        x (int): X-coordinate of the layout's origin.
        y (int): Y-coordinate of the layout's origin.
        spacing (int): Pixels between adjacent elements.
        elements (List[UIElement]): Child elements in the layout.
        rect (pygame.Rect): Bounding rectangle covering all children.
    """
    def __init__(self, x: int, y: int, spacing: int = 10) -> None:
        """
        Initialize a HorizontalLayout at a given position.

        Args:
            x (int): X-coordinate for layout origin.
            y (int): Y-coordinate for layout origin.
            spacing (int, optional): Space in pixels between elements. Defaults to 10.
        """
        self.x = x
        self.y = y
        self.spacing = spacing
        # List of managed UI elements or nested layouts
        self.elements: List[Any] = []
        # Bounding rect to track combined size of children
        self.rect = pygame.Rect(x, y, 0, 0)

    def add(self, element: Any) -> None:
        """
        Add a new element to the layout, position it, and update bounds.

        If the element provides set_position, use it; otherwise adjust rect directly.

        Args:
            element: UIElement or any object with a .rect attribute and optional set_position().
        """
        # Determine offset based on existing elements and spacing
        total_width = self._accumulated_width()

        # Use element's set_position if available, else set rect directly
        if hasattr(element, "set_position"):
            element.set_position(self.x + total_width, self.y)
        else:
            element.rect.topleft = (self.x + total_width, self.y)

        self.elements.append(element)
        self.recalculate_rect()

    def _accumulated_width(self) -> int:
        """
        Compute total width of existing elements plus spacing between them.

        Returns:
            int: Combined width in pixels.
        """
        total = 0
        for el in self.elements:
            total += el.rect.width
        # Add spacing between each pair of elements
        total += self.spacing * len(self.elements)
        return total

    def recalculate_rect(self) -> None:
        """
        Recalculate the bounding rectangle size based on child dimensions.
        """
        if not self.elements:
            # No children, keep zero size
            self.rect.size = (0, 0)
            return

        # Total width excluding trailing spacing
        width = self._accumulated_width() - self.spacing
        # Maximum height among children
        height = max(el.rect.height for el in self.elements)
        self.rect.width = width
        self.rect.height = height

    def set_position(self, x: int, y: int) -> None:
        """
        Move layout origin and reposition all contained elements accordingly.

        Args:
            x (int): New X-coordinate for layout origin.
            y (int): New Y-coordinate for layout origin.
        """
        dx = x - self.x
        dy = y - self.y
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

        # Move each child by the same offset, maintaining spacing
        current_x_offset = 0
        for el in self.elements:
            new_x = x + current_x_offset
            new_y = y
            if hasattr(el, "set_position"):
                el.set_position(new_x, new_y)
            else:
                el.rect.topleft = (new_x, new_y)
            current_x_offset += el.rect.width + self.spacing

    def get_elements(self) -> List[Any]:
        """
        Retrieve a flat list of all elements, including nested layout children.

        Returns:
            List[Any]: List of contained elements or nested element lists.
        """
        flat: List[Any] = []
        for el in self.elements:
            # If nested layout, extend its children
            if hasattr(el, "get_elements"):
                flat.extend(el.get_elements())
            else:
                flat.append(el)
        return flat
