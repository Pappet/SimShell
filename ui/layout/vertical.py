import pygame

class VerticalLayout:
    def __init__(self, x, y, spacing=10, debug_console=None):
        self.debug_console = debug_console
        self.x = x
        self.y = y
        self.spacing = spacing
        self.elements = []
        self.rect = pygame.Rect(x, y, 0, 0)

    def add(self, element):
        # Berechne den vertikalen Offset basierend auf der bereits vorhandenen Elementehöhe.
        total_height = self._accumulated_height()

        # Wenn das Element selbst ein Layout (also einen eigenen set_position-Mechanismus) besitzt,
        # lasse es selbst seine internen Elemente setzen.
        if hasattr(element, "set_position"):
            element.set_position(self.x, self.y + total_height)
        else:
            element.rect.topleft = (self.x, self.y + total_height)

        if self.debug_console:
            self.debug_console.log(f"Adding element at position: {element.rect.topleft}")
        self.elements.append(element)
        self.recalculate_rect()

    def _accumulated_height(self):
        # Summiert die Höhen aller bisher hinzugefügten Elemente inkl. Spacing
        total = 0
        for el in self.elements:
            total += el.rect.height
        # Addiere das Spacing zwischen den Elementen (nicht nach dem letzten Element)
        total += self.spacing * len(self.elements)
        return total

    def recalculate_rect(self):
        # Bestimme Breite und Höhe des Layout-Containers anhand der enthaltenen Elemente.
        width = max((el.rect.width for el in self.elements), default=0)
        height = self._accumulated_height() - (self.spacing if self.elements else 0)
        self.rect.width = width
        self.rect.height = height

    def get_elements(self):
        flat = []
        for el in self.elements:
            if hasattr(el, "get_elements"):
                flat.extend(el.get_elements())
            else:
                flat.append(el)
        return flat

    def set_position(self, x, y):
        # Verschiebe das Layout und positioniere alle enthaltenen Elemente relativ zum neuen Ursprung.
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)
        current_y_offset = 0
        for el in self.elements:
            if hasattr(el, "set_position"):
                el.set_position(x, y + current_y_offset)
            else:
                el.rect.topleft = (x, y + current_y_offset)
            # Aktualisiere den Offset für das nächste Element.
            current_y_offset += el.rect.height + self.spacing