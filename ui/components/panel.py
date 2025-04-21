import pygame
import setup.config as Config
from themes.theme_manager import get_color

class Panel:
    """
    A container grouping UI elements within a panel with background and border.
    Automatically resizes to fit child elements unless fixed size is desired.

    Parameters:
        x, y        : Position of the panel.
        width, height: Optional minimum size. If None, starts at 0 and grows to fit.
        background_key: Theme key for background color.
        border_key    : Theme key for border color.
        padding       : Space in pixels between border and child elements.
        debug_console : Optional logger for debugging.
    """
    def __init__(self, x, y, width=None, height=None,
                 background_key='panel_background',
                 border_key='border',
                 padding=Config.ui["default"]["padding"]):
        init_w = width or 0
        init_h = height or 0
        self.rect = pygame.Rect(x, y, init_w, init_h)
        self.background_key = background_key
        self.border_key = border_key
        self.padding = padding
        self.elements = []
        self.child_positions = []

    def add(self, element):
        """
        Adds a UI element or layout inside the panel, applies padding, and resizes panel.
        """
        # Original local coords of element relative to panel interior
        local_x, local_y = element.rect.x, element.rect.y
        # Apply padding
        rel_x = local_x + self.padding
        rel_y = local_y + self.padding
        # Position element absolutely
        if hasattr(element, 'set_position'):
            element.set_position(self.rect.x + rel_x,
                                 self.rect.y + rel_y)
        else:
            element.rect.topleft = (self.rect.x + rel_x,
                                    self.rect.y + rel_y)
        # Store for resize and reposition
        self.elements.append(element)
        self.child_positions.append((rel_x, rel_y))
        # Resize panel to fit all children with padding
        self._resize_to_children()

    def _resize_to_children(self):
        """
        Adjust panel size to the bounding box of all child elements plus padding.
        """
        max_w = 0
        max_h = 0
        for el, (rel_x, rel_y) in zip(self.elements, self.child_positions):
            w = rel_x + el.rect.width
            h = rel_y + el.rect.height
            if w > max_w:
                max_w = w
            if h > max_h:
                max_h = h
        base_w, base_h = self.rect.width, self.rect.height
        # Add right/bottom padding
        new_w = max(base_w, max_w + self.padding)
        new_h = max(base_h, max_h + self.padding)
        self.rect.width = new_w
        self.rect.height = new_h

    def get_elements(self):
        """
        Returns all nested UI elements flattened.
        """
        flat = []
        for el in self.elements:
            if hasattr(el, 'get_elements'):
                flat.extend(el.get_elements())
            else:
                flat.append(el)
        return flat

    def handle_event(self, event):
        """
        Propagate events to children.
        """
        for el in self.get_elements():
            if hasattr(el, 'handle_event'):
                el.handle_event(event)

    def update(self, mouse_pos):
        """
        Update state (e.g. hover) of children.
        """
        for el in self.get_elements():
            if hasattr(el, 'update'):
                el.update(mouse_pos)

    def draw(self, surface):
        """
        Draw background, border, then children.
        """
        # Background
        pygame.draw.rect(surface,
                         get_color(self.background_key),
                         self.rect)
        # Border
        pygame.draw.rect(surface,
                         get_color(self.border_key),
                         self.rect,
                         2)
        # Draw child elements
        for el in self.get_elements():
            if hasattr(el, 'draw'):
                el.draw(surface)

    def set_position(self, x, y):
        """
        Move panel and reposition children, respecting padding offsets.
        """
        self.rect.topleft = (x, y)
        for element, (rel_x, rel_y) in zip(self.elements, self.child_positions):
            target_x = x + rel_x
            target_y = y + rel_y
            if hasattr(element, 'set_position'):
                element.set_position(target_x, target_y)
            else:
                element.rect.topleft = (target_x, target_y)
