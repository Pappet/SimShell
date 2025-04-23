# ui/components/table.py

import pygame
from ui.components.label import Label
from ui.components.base import UIElement
from themes.theme_manager import get_color

class Table(UIElement):
    def __init__(self, x, y, column_widths, row_height, headers=None, font_size=None, font_name=None):
        super().__init__()
        self.x, self.y = x, y
        self.col_widths = column_widths
        self.row_height = row_height
        self.headers = headers or []
        self.rows = []       # Liste von Zeilen, jede Zeile ist Liste von Strings
        self.font_size = font_size
        self.font_name = font_name

        # vorbereitete Label‑Objekte
        self._create_header_labels()

    def _create_header_labels(self):
        self.header_labels = []
        if not self.headers: 
            return
        dx = self.x
        for i, text in enumerate(self.headers):
            lbl = Label(text, (dx + 5, self.y + 5), self.font_size, self.font_name)
            self.header_labels.append(lbl)
            dx += self.col_widths[i]

    def add_row(self, values):
        """Fügt eine neue Zeile hinzu. Länge muss zu Anzahl Spalten passen."""
        if len(values) != len(self.col_widths):
            raise ValueError("Spaltenanzahl stimmt nicht überein")
        self.rows.append(values)

    def clear(self):
        """Löscht alle Zeilen."""
        self.rows.clear()

    def draw(self, surface):
        # 1) Header‑Zeile zeichnen (rahmen + Hintergrund)
        if self.headers:
            total_width = sum(self.col_widths)
            hdr_rect = pygame.Rect(self.x, self.y, total_width, self.row_height)
            pygame.draw.rect(surface, get_color("panel_bg"), hdr_rect)
            pygame.draw.rect(surface, get_color("border"), hdr_rect, 1)
            for lbl in self.header_labels:
                lbl.draw(surface)

        # 2) Daten‑Zeilen zeichnen
        for ridx, row in enumerate(self.rows):
            y_off = self.y + (ridx + (1 if self.headers else 0)) * self.row_height
            dx = self.x
            for cidx, cell in enumerate(row):
                cell_rect = pygame.Rect(dx, y_off, self.col_widths[cidx], self.row_height)
                # wechselnde Zeilenfarbe optional:
                bg = get_color("background") if ridx % 2 == 0 else get_color("panel_bg")
                pygame.draw.rect(surface, bg, cell_rect)
                pygame.draw.rect(surface, get_color("border"), cell_rect, 1)
                # Text zentriert
                lbl = Label(str(cell), (dx + 5, y_off + 5), self.font_size, self.font_name)
                lbl.draw(surface)
                dx += self.col_widths[cidx]

    def handle_event(self, event):
        # falls Scroll oder Klick nötig, hier abfangen
        pass

    def update(self, mouse_pos):
        # falls Hover‑Effekte o.ä.
        pass
