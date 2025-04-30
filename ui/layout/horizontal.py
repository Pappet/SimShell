import pygame
import logging
from typing import List, Any, Tuple

import setup.config as Config
from ui.components.base import UIElement

logger = logging.getLogger(__name__)

class HorizontalLayout:
    """
    Layout manager that arranges UI elements side by side with configurable spacing and vertical alignment.

    Attributes:
        x (int): X-coordinate of layout origin.
        y (int): Y-coordinate of layout origin.
        spacing (int): Horizontal space in pixels between elements.
        align (str): Vertical alignment for children: 'top', 'center', or 'bottom'.
        elements (List[Any]): Child UI elements or nested layouts.
        rect (pygame.Rect): Bounding rectangle covering all children.
    """
    def __init__(
        self,
        x: int,
        y: int,
        spacing: int = Config.ui["default"]["spacing"],
        align: str = 'top'
    ) -> None:
        """
        Initialize a HorizontalLayout at a given position.

        Args:
            x (int): X-coordinate for layout origin.
            y (int): Y-coordinate for layout origin.
            spacing (int, optional): Horizontal space between elements. Defaults to config spacing.
            align (str, optional): Vertical alignment of children ('top', 'center', 'bottom'). Defaults to 'top'.
        """
        self.x = x
        self.y = y
        self.spacing = spacing
        self.align = align
        self.elements: List[Any] = []
        self.rect = pygame.Rect(x, y, 0, 0)
        logger.debug("HorizontalLayout initialized at (%d, %d) with spacing %d and align '%s'", x, y, spacing, align)

    def add(self, element: Any) -> None:
        """
        Add an element to the layout and update positions and bounding rect.

        Args:
            element: UIElement or nested layout with rect attribute.
        """
        self.elements.append(element)
        self.recalculate_rect()

    def _accumulated_width(self) -> int:
        """
        Compute total width of elements plus spacing between them.

        Returns:
            int: Combined width in pixels.
        """
        total = sum(el.rect.width for el in self.elements)
        total += self.spacing * (len(self.elements) - 1 if self.elements else 0)
        return total

    def recalculate_rect(self) -> None:
        """
        Recompute layout bounds and reposition all child elements based on alignment and spacing.
        """
        # Determine total width and maximum child height
        total_width = self._accumulated_width()
        max_height = max((el.rect.height for el in self.elements), default=0)
        # Update layout rect size
        self.rect.width = total_width
        self.rect.height = max_height

        # Position children horizontally with alignment
        current_x = self.x
        for el in self.elements:
            # Determine vertical offset based on alignment
            if self.align == 'center':
                y_offset = self.y + (self.rect.height - el.rect.height) // 2
            elif self.align == 'bottom':
                y_offset = self.y + self.rect.height - el.rect.height
            else:  # 'top'
                y_offset = self.y

            x_offset = current_x
            # Position using element's set_position if available
            if hasattr(el, 'set_position'):
                el.set_position(x_offset, y_offset)
            else:
                el.rect.topleft = (x_offset, y_offset)
            # Advance horizontal position for next element
            current_x += el.rect.width + self.spacing

        logger.debug("HorizontalLayout recalculated: rect=%s", self.rect)

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
        logger.debug("HorizontalLayout moved to (%d, %d)", x, y)

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
