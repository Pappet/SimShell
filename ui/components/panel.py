"""
Module ui/components/panel.py

Defines Panel UIElement as a container for grouping other UI components.
Supports background, border, padding, dynamic resizing based on children,
and event propagation to nested elements.
"""

import pygame
from typing import Tuple

import setup.config as Config
from themes.theme_manager import get_color
from ui.components.base import UIElement


class UIPanel(UIElement):
    """
    Container for grouping UI elements with background, border, and padding.

    Automatically resizes to accommodate children unless fixed dimensions are provided.
    Provides event propagation, update, and drawing for nested elements.
    """
    def __init__(
        self,
        x: int,
        y: int,
        width: int = None,
        height: int = None,
        background_key: str = "panel_background",
        border_key: str = "border",
        padding: int = None
    ) -> None:
        """
        Initialize a Panel instance.

        Args:
            x (int): X-coordinate of panel's top-left corner.
            y (int): Y-coordinate of panel's top-left corner.
            width (int, optional): Minimum width; defaults to zero if None.
            height (int, optional): Minimum height; defaults to zero if None.
            background_key (str): Theme key for panel background color.
            border_key (str): Theme key for panel border color.
            padding (int, optional): Space in pixels between border and children;
                uses default UI padding if None.
        """
        # Set base size to provided values or zero
        w = width or 0
        h = height or 0
        super().__init__(x, y, w, h)

        # Theme keys and padding configuration
        self.background_key = background_key
        self.border_key = border_key
        self.padding = padding if padding is not None else Config.ui["default"]["padding"]

        # Child elements and their positions relative to panel
        self.elements: list[UIElement] = []
        self.child_positions: list[Tuple[int, int]] = []

    def add(self, element: UIElement) -> None:
        """
        Add a child UI element to the panel and update layout.

        Args:
            element (UIElement): The UI component to add.
        """
        # Calculate element's relative offset inside panel with padding
        rel_x = element.x + self.padding
        rel_y = element.y + self.padding

        # Position element at absolute coordinates based on panel origin
        element.set_position(self.x + rel_x, self.y + rel_y)

        # Store element and its relative position for resizing
        self.elements.append(element)
        self.child_positions.append((rel_x, rel_y))

        # Resize panel to fit all children
        self._resize_to_children()

    def _resize_to_children(self) -> None:
        """
        Adjust panel dimensions to enclose all child elements plus padding.
        """
        if not self.elements:
            return

        # Compute maximum extents required by children
        max_w = 0
        max_h = 0
        for el, (rel_x, rel_y) in zip(self.elements, self.child_positions):
            max_w = max(max_w, rel_x + el.rect.width)
            max_h = max(max_h, rel_y + el.rect.height)

        # Determine target size including padding
        target_w = max(self.width, max_w + self.padding)
        target_h = max(self.height, max_h + self.padding)

        # Apply new size to panel and update rect
        self.width = target_w
        self.height = target_h
        self.rect.size = (self.width, self.height)

    def get_elements(self) -> list[UIElement]:
        """
        Retrieve a flat list of all nested UI elements.

        Returns:
            list[UIElement]: Flattened list of panel's child elements,
            including children of nested Panels.
        """
        flat: list[UIElement] = []
        for el in self.elements:
            # If element contains its own children (e.g., nested Panel)
            if hasattr(el, "get_elements"):
                flat.extend(el.get_elements())
            else:
                flat.append(el)
        return flat

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Propagate a Pygame event to all nested UI elements.

        Args:
            event (pygame.event.Event): The event to dispatch.
        """
        for el in self.get_elements():
            el.handle_event(event)

    def update(self, mouse_pos: tuple[int, int]) -> None:
        """
        Update state of nested UI elements (e.g., hover effects).

        Args:
            mouse_pos (tuple[int,int]): Current mouse coordinates.
        """
        for el in self.get_elements():
            el.update(mouse_pos)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw panel background, border, and then all child elements.

        Args:
            surface (pygame.Surface): Drawing target for rendering.
        """
        # Draw background and border using theme colors
        bg_color = get_color(self.background_key)
        border_color = get_color(self.border_key)
        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(
            surface,
            border_color,
            self.rect,
            Config.ui["default"]["border_width"]
        )

        # Render each nested element
        for el in self.get_elements():
            el.draw(surface)

    def set_position(self, x: int, y: int) -> None:
        """
        Move panel and adjust positions of all child elements by same offset.

        Args:
            x (int): New X-coordinate for panel.
            y (int): New Y-coordinate for panel.
        """
        # Compute offset difference
        dx = x - self.x
        dy = y - self.y
        # Update panel position
        super().set_position(x, y)

        # Move children by the panel's offset
        for el in self.elements:
            el.set_position(el.x + dx, el.y + dy)