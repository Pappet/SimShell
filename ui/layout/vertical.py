"""
Module ui/layouts/vertical_layout.py

Defines VerticalLayout for arranging UI elements in a vertical column with configurable spacing and horizontal alignment.
Automatically positions added elements, recalculates container bounds, and propagates layout updates when moved.
Supports nested layouts and event/update propagation to contained elements.
"""

import pygame
import logging
from typing import List, Any, Tuple

import setup.config as Config
from ui.components.base import UIElement

logger = logging.getLogger(__name__)


class VerticalLayout:
    """
    Layout manager that stacks UI elements vertically.

    Attributes:
        x (int): X-coordinate of layout origin.
        y (int): Y-coordinate of layout origin.
        spacing (int): Vertical space in pixels between elements.
        align (str): Horizontal alignment for children: 'left', 'center', or 'right'.
        elements (List[Any]): Child UI elements or nested layouts.
        rect (pygame.Rect): Bounding rectangle covering all children.
    """
    def __init__(
        self,
        x: int,
        y: int,
        spacing: int = Config.ui["default"]["spacing"],
        align: str = 'left'
    ) -> None:
        """
        Initialize a VerticalLayout at a given position.

        Args:
            x (int): X-coordinate for layout origin.
            y (int): Y-coordinate for layout origin.
            spacing (int, optional): Vertical space between elements. Defaults to config spacing.
            align (str, optional): Horizontal alignment of children ('left', 'center', 'right').
        """
        self.x = x
        self.y = y
        self.spacing = spacing
        self.align = align
        self.elements: List[Any] = []
        # Bounding rect initialized with zero size
        self.rect = pygame.Rect(x, y, 0, 0)
        logger.debug("VerticalLayout initialized at (%d, %d) with spacing %d and align '%s'", x, y, spacing, align)

    def add(self, element: Any) -> None:
        """
        Add an element to the layout and update positions and bounding rect.

        Args:
            element: UIElement or nested layout with rect attribute.
        """
        self.elements.append(element)
        self.recalculate_rect()

    def _accumulated_height(self) -> int:
        """
        Compute total height of elements plus spacing between them.

        Returns:
            int: Combined height in pixels.
        """
        total = sum(el.rect.height for el in self.elements)
        # Add spacing between elements (n-1 gaps)
        total += self.spacing * (len(self.elements) - 1 if self.elements else 0)
        return total

    def recalculate_rect(self) -> None:
        """
        Recompute layout bounds and reposition all child elements based on alignment and spacing.
        """
        # Determine maximum child width and total height
        max_width = max((el.rect.width for el in self.elements), default=0)
        total_height = self._accumulated_height()
        # Update layout rect size
        self.rect.width = max_width
        self.rect.height = total_height
        # Position children vertically with alignment
        current_y = self.y
        for el in self.elements:
            # Determine horizontal offset based on alignment
            if self.align == 'center':
                x_offset = self.x + (self.rect.width - el.rect.width) // 2
            elif self.align == 'right':
                x_offset = self.x + self.rect.width - el.rect.width
            else:  # 'left'
                x_offset = self.x
            # Position using element's set_position if available
            if hasattr(el, 'set_position'):
                el.set_position(x_offset, current_y)
            else:
                el.rect.topleft = (x_offset, current_y)
            # Advance vertical position for next element
            current_y += el.rect.height + self.spacing
        logger.debug("VerticalLayout recalculated: rect=%s", self.rect)

    def set_position(self, x: int, y: int) -> None:
        """
        Move the layout origin and reposition all children accordingly.

        Args:
            x (int): New X-coordinate for layout origin.
            y (int): New Y-coordinate for layout origin.
        """
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)
        self.recalculate_rect()
        logger.debug("VerticalLayout moved to (%d, %d)", x, y)

    def get_elements(self) -> List[Any]:
        """
        Retrieve a flat list of all contained UIElements, including nested layouts.

        Returns:
            List[Any]: Flattened list of child elements.
        """
        flat: List[Any] = []
        for el in self.elements:
            if hasattr(el, 'get_elements'):
                flat.extend(el.get_elements())
            else:
                flat.append(el)
        return flat

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Propagate an event to all nested elements supporting handle_event.

        Args:
            event (pygame.event.Event): The event to dispatch.
        """
        for el in self.get_elements():
            if hasattr(el, 'handle_event'):
                try:
                    el.handle_event(event)
                except Exception:
                    logger.exception("Error in handle_event of %s", el)

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Update all nested elements (e.g., for hover states).

        Args:
            mouse_pos (Tuple[int,int]): Current mouse coordinates.
        """
        for el in self.get_elements():
            if hasattr(el, 'update'):
                try:
                    el.update(mouse_pos)
                except Exception:
                    logger.exception("Error in update of %s", el)
