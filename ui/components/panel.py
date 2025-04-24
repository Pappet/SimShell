# ui/components/panel.py

import pygame
import setup.config as Config
from themes.theme_manager import get_color
from ui.components.base import UIElement

class Panel(UIElement):
    """
    Container for grouping UI elements with background and border.
    Automatically resizes to fit children unless fixed size is specified.
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
    ):
        """
        Initialize the panel.

        Args:
            x (int): X position.
            y (int): Y position.
            width (int, optional): Minimum width. Defaults to 0 if None.
            height (int, optional): Minimum height. Defaults to 0 if None.
            background_key (str): Theme key for background color.
            border_key (str): Theme key for border color.
            padding (int, optional): Space between border and children.
        """
        w = width or 0
        h = height or 0
        super().__init__(x, y, w, h)

        self.background_key = background_key
        self.border_key = border_key
        self.padding = padding if padding is not None else Config.ui["default"]["padding"]

        self.elements = []
        self.child_positions = []

    def add(self, element: UIElement):
        """
        Add a child element to the panel and adjust layout.
        """
        # Calculate relative position inside panel
        local_x = element.rect.x
        local_y = element.rect.y
        rel_x = local_x + self.padding
        rel_y = local_y + self.padding

        # Position element absolutely
        element.set_position(self.x + rel_x, self.y + rel_y)

        self.elements.append(element)
        self.child_positions.append((rel_x, rel_y))

        # Resize panel to fit new child
        self._resize_to_children()

    def _resize_to_children(self):
        """
        Adjust panel size to fit all child elements plus padding.
        """
        if not self.elements:
            return

        max_w = max(rel_x + el.rect.width for el, (rel_x, _) in zip(self.elements, self.child_positions))
        max_h = max(rel_y + el.rect.height for el, (_, rel_y) in zip(self.elements, self.child_positions))

        target_w = max(self.width, max_w + self.padding)
        target_h = max(self.height, max_h + self.padding)

        self.width = target_w
        self.height = target_h
        self.rect.size = (self.width, self.height)

    def get_elements(self):
        """
        Return all nested UI elements in a flat list.
        """
        flat = []
        for el in self.elements:
            if hasattr(el, "get_elements"):
                flat.extend(el.get_elements())
            else:
                flat.append(el)
        return flat

    def handle_event(self, event: pygame.event.Event):
        """
        Propagate events to child elements.
        """
        for el in self.get_elements():
            el.handle_event(event)

    def update(self, mouse_pos: tuple[int, int]):
        """
        Update child elements (e.g., hover states).
        """
        for el in self.get_elements():
            el.update(mouse_pos)

    def draw(self, surface: pygame.Surface):
        """
        Draw the panel background, border, and child elements.
        """
        bg_color = get_color(self.background_key)
        border_color = get_color(self.border_key)

        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(
            surface,
            border_color,
            self.rect,
            Config.ui["default"]["border_width"]
        )

        for el in self.get_elements():
            el.draw(surface)

    def set_position(self, x: int, y: int):
        """
        Move panel and reposition all children by the same offset.
        """
        dx = x - self.x
        dy = y - self.y
        super().set_position(x, y)

        for el in self.elements:
            el.set_position(el.x + dx, el.y + dy)
