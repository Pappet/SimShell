# ui/components/table.py

"""
Table UI component for displaying tabular data with optional headers and embedded widgets.
"""

import pygame
from typing import Any, List, Tuple
from ui.components.base import UIElement
from ui.components.label import Label
from themes.theme_manager import get_color
import setup.config as Config

class Table(UIElement):
    """
    Displays data in rows and columns, with optional header row and support for UIElement cells.
    """
    def __init__(
        self,
        x: int,
        y: int,
        column_widths: List[int],
        row_height: int,
        headers: List[str] = None,
        font_size: int = None,
        font_name: str = None
    ) -> None:
        """
        Initialize the Table component.

        Args:
            x (int): X position.
            y (int): Y position.
            column_widths (List[int]): Widths for each column.
            row_height (int): Height for each row.
            headers (List[str], optional): Header texts. Defaults to None.
            font_size (int, optional): Font size for cell text.
            font_name (str, optional): Font name for cell text.
        """
        total_width = sum(column_widths)
        initial_rows = 1 if headers else 0
        initial_height = initial_rows * row_height
        super().__init__(x, y, total_width, initial_height)

        self.column_widths = column_widths
        self.row_height = row_height
        self.headers = headers or []
        self.rows: List[List[Any]] = []

        self.font_name = font_name or Config.fonts['default']['name']
        self.font_size = font_size or Config.fonts['default']['size']

        # Prepare header labels
        self.header_labels: List[Label] = []
        if self.headers:
            self._create_header_labels()

    def _create_header_labels(self) -> None:
        """
        Create Label objects for the header row.
        """
        self.header_labels.clear()
        dx = self.x
        for idx, text in enumerate(self.headers):
            lbl = Label(
                text=text,
                x=dx + 5,
                y=self.y + 5,
                font_size=self.font_size,
                font_name=self.font_name
            )
            self.header_labels.append(lbl)
            dx += self.column_widths[idx]

    def add_row(self, values: List[Any]) -> None:
        """
        Add a new data row. Values can be primitives or UIElement instances.

        Args:
            values (List[Any]): Cell values/widgets for the new row.
        """
        if len(values) != len(self.column_widths):
            raise ValueError("Column count mismatch")
        self.rows.append(values)
        total_rows = len(self.rows) + (1 if self.headers else 0)
        self.height = total_rows * self.row_height
        self.rect.height = self.height

    def clear(self) -> None:
        """
        Remove all data rows, keeping headers intact.
        """
        self.rows.clear()
        self.height = (1 if self.headers else 0) * self.row_height
        self.rect.height = self.height

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the table: header row, data rows with alternating backgrounds, and embedded UIElements.
        """
        border_w = Config.ui['default']['border_width']

        # Draw headers
        if self.headers:
            hdr_rect = pygame.Rect(self.x, self.y, self.width, self.row_height)
            pygame.draw.rect(surface, get_color('panel_bg'), hdr_rect)
            pygame.draw.rect(surface, get_color('border'), hdr_rect, border_w)
            for lbl in self.header_labels:
                lbl.draw(surface)

        # Draw rows
        for ridx, row in enumerate(self.rows):
            y_off = self.y + (ridx + (1 if self.headers else 0)) * self.row_height
            dx = self.x
            for cidx, cell in enumerate(row):
                col_w = self.column_widths[cidx]
                cell_rect = pygame.Rect(dx, y_off, col_w, self.row_height)
                bg_key = 'background' if ridx % 2 == 0 else 'panel_bg'
                pygame.draw.rect(surface, get_color(bg_key), cell_rect)
                pygame.draw.rect(surface, get_color('border'), cell_rect, border_w)

                if isinstance(cell, UIElement):
                    cell.set_position(dx + 5, y_off + 5)
                    cell.draw(surface)
                else:
                    text_lbl = Label(
                        text=str(cell),
                        x=dx + 5,
                        y=y_off + 5,
                        font_size=self.font_size,
                        font_name=self.font_name
                    )
                    text_lbl.draw(surface)
                dx += col_w

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Forward events to any embedded widgets in the table.
        """
        for row in self.rows:
            for cell in row:
                if isinstance(cell, UIElement):
                    cell.handle_event(event)

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Update hover or other interactive state for embedded widgets.
        """
        for row in self.rows:
            for cell in row:
                if isinstance(cell, UIElement):
                    cell.update(mouse_pos)
