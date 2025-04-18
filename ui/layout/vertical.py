import pygame
import logging

logger = logging.getLogger(__name__)

class VerticalLayout:
    def __init__(self, x, y, spacing=10, align='left'):
        """
        A vertical layout for UI elements, with optional horizontal alignment.

        Args:
            x (int): X position of layout origin.
            y (int): Y position of layout origin.
            spacing (int): Vertical spacing between elements.
            align (str): Horizontal alignment: 'left', 'center', or 'right'.
        """
        self.x = x
        self.y = y
        self.spacing = spacing
        self.align = align
        self.elements = []
        self.rect = pygame.Rect(x, y, 0, 0)

    def add(self, element):
        # Add element and recalculate positions and size
        self.elements.append(element)
        self.recalculate_rect()

    def _accumulated_height(self):
        total = 0
        for el in self.elements:
            total += el.rect.height
        total += self.spacing * (len(self.elements) - 1 if self.elements else 0)
        return total

    def recalculate_rect(self):
        # Compute width and height
        max_width = max((el.rect.width for el in self.elements), default=0)
        total_height = self._accumulated_height()
        self.rect.width = max_width
        self.rect.height = total_height

        # Reposition all children
        current_y = self.y
        for el in self.elements:
            # Horizontal alignment
            if self.align == 'center':
                x_offset = self.x + (self.rect.width - el.rect.width) // 2
            elif self.align == 'right':
                x_offset = self.x + self.rect.width - el.rect.width
            else:  # left
                x_offset = self.x

            # Position element
            if hasattr(el, 'set_position'):
                el.set_position(x_offset, current_y)
            else:
                el.rect.topleft = (x_offset, current_y)

            current_y += el.rect.height + self.spacing

    def get_elements(self):
        flat = []
        for el in self.elements:
            if hasattr(el, 'get_elements'):
                flat.extend(el.get_elements())
            else:
                flat.append(el)
        return flat

    def set_position(self, x, y):
        # Move layout and recalc positions
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)
        self.recalculate_rect()

    def handle_event(self, event):
        for el in self.get_elements():
            if hasattr(el, 'handle_event'):
                el.handle_event(event)

    def update(self, mouse_pos):
        for el in self.get_elements():
            if hasattr(el, 'update'):
                el.update(mouse_pos)
