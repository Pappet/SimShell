# ui/components/base.py

import pygame

class UIElement:
    """Basisklasse für alle UI-Komponenten."""
    def __init__(self, x: int, y: int, width: int = 0, height: int = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # Rechteck, um Klicks/Mouseover zu erkennen
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface: pygame.Surface):
        """
        Muss überschrieben werden. Hier rendert das Element sich selbst.
        """
        raise NotImplementedError

    def handle_event(self, event: pygame.event.Event):
        """
        Wird für jedes Event aufgerufen. Komponenten mit Klick- oder
        Eingabe-Logik kümmert sich hierum.
        """
        pass

    def update(self, mouse_pos: tuple[int, int]):
        """
        Wird einmal pro Frame aufgerufen, mit der aktuellen Mausposition.
        Für Hover-Effekte o.ä.
        """
        pass

    def set_position(self, x: int, y: int):
        """Position dynamisch anpassen (z.B. beim Layout)."""
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)

    def contains(self, point: tuple[int, int]) -> bool:
        """Hilfsmethode: erkennt, ob ein Punkt im Element ist."""
        return self.rect.collidepoint(point)
