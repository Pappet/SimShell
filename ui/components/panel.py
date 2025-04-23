# ui/components/panel.py

import pygame
import setup.config as Config
from ui.components.base import UIElement
from themes.theme_manager import get_color

class Panel(UIElement):
    """
    Container für UI-Elemente mit Hintergrund und Rahmen.
    Passt seine Größe automatisch an die Kinder an, sofern keine min.
    Breite/Höhe angegeben sind.
    """
    def __init__(
        self,
        x, y,
        width=None, height=None,
        background_key='panel_background',
        border_key='border',
        padding=None
    ):
        # min. Größe oder 0
        w = width or 0
        h = height or 0
        super().__init__(x, y, w, h)

        self.background_key = background_key
        self.border_key = border_key
        # Padding aus Config, falls none reingegeben
        self.padding = padding if padding is not None else Config.ui["default"]["padding"]

        self.elements = []          # direkte Kinder
        self.child_positions = []   # relative Positionen innerhalb des Panels

    def add(self, element: UIElement):
        """
        Fügt ein Kind-Element hinzu. Das Element muss vorher bereits
        lokale Koordinaten (element.rect.x/y) definiert haben.
        Wir verschieben es um Padding, positionieren und merken uns die Relativ-Pos.
        """
        # lokale Koordinaten relativ zum Panel-Innenbereich
        rel_x = element.rect.x + self.padding
        rel_y = element.rect.y + self.padding

        # absolute Position
        element.set_position(self.x + rel_x, self.y + rel_y)

        self.elements.append(element)
        self.child_positions.append((rel_x, rel_y))

        # Panel-Größe anpassen
        self._resize_to_children()

    def _resize_to_children(self):
        max_w = max((rel_x + el.rect.width) for el, (rel_x, _) in zip(self.elements, self.child_positions)) if self.elements else 0
        max_h = max((rel_y + el.rect.height) for el, (_, rel_y) in zip(self.elements, self.child_positions)) if self.elements else 0

        # rechne padding am rechten und unteren Rand mit ein
        target_w = max(self.width,  max_w + self.padding)
        target_h = max(self.height, max_h + self.padding)

        self.width  = target_w
        self.height = target_h
        self.rect.size = (self.width, self.height)

    def get_elements(self):
        """Alle verschachtelten UI-Elemente als flache Liste."""
        flat = []
        for el in self.elements:
            if hasattr(el, 'get_elements'):
                flat.extend(el.get_elements())
            else:
                flat.append(el)
        return flat

    def handle_event(self, event):
        for el in self.get_elements():
            el.handle_event(event)

    def update(self, mouse_pos):
        for el in self.get_elements():
            el.update(mouse_pos)

    def draw(self, surface):
        # Hintergrund
        pygame.draw.rect(surface,
                         get_color(self.background_key),
                         self.rect)
        # Rahmen
        pygame.draw.rect(surface,
                         get_color(self.border_key),
                         self.rect,
                         Config.ui["default"]["border_width"])
        # Kinder zeichnen
        for el in self.get_elements():
            el.draw(surface)

    def set_position(self, x, y):
        """
        Panel und alle Kinder verschieben.
        """
        dx = x - self.x
        dy = y - self.y
        super().set_position(x, y)

        for el, (rel_x, rel_y) in zip(self.elements, self.child_positions):
            el.set_position(x + rel_x, y + rel_y)
