import pygame

class HorizontalLayout:
    def __init__(self, x, y, spacing=10, debug_console=None):
        self.debug_console = debug_console
        self.x = x
        self.y = y
        self.spacing = spacing
        self.elements = []
        self.rect = pygame.Rect(x, y, 0, 0)

    def add(self, element):
        total_width = self._accumulated_width()

        # Nutze den set_position Mechanismus des Elements, falls vorhanden.
        if hasattr(element, "set_position"):
            element.set_position(self.x + total_width, self.y)
        else:
            element.rect.topleft = (self.x + total_width, self.y)

        if self.debug_console:
            self.debug_console.log(f"Adding element at position: {element.rect.topleft}")
        self.elements.append(element)
        self.recalculate_rect()

    def _accumulated_width(self):
        # Berechnet die Summe der Breiten der bereits hinzugefügten Elemente
        # plus das Spacing zwischen diesen Elementen.
        total = 0
        for el in self.elements:
            total += el.rect.width
        total += self.spacing * len(self.elements)
        return total

    def recalculate_rect(self):
        # Berechnet die Gesamtbreite und -höhe des Layout-Containers.
        width = self._accumulated_width() - (self.spacing if self.elements else 0)
        height = max((el.rect.height for el in self.elements), default=0)
        self.rect.width = width
        self.rect.height = height

    def set_position(self, x, y):
        # Verschiebt das Layout an die neue Position und positioniert alle enthaltenen
        # Elemente relativ zu diesem neuen Ursprung.
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)
        current_x_offset = 0
        for el in self.elements:
            if hasattr(el, "set_position"):
                el.set_position(x + current_x_offset, y)
            else:
                el.rect.topleft = (x + current_x_offset, y)
            current_x_offset += el.rect.width + self.spacing

    def get_elements(self):
        # Gibt alle Elemente zurück; bei verschachtelten Layouts werden
        # deren interne Elemente ebenfalls flach zurückgegeben.
        flat = []
        for el in self.elements:
            if hasattr(el, "get_elements"):
                flat.extend(el.get_elements())
            else:
                flat.append(el)
        return flat