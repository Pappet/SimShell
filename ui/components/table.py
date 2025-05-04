"""
Module ui/components/table.py

Defines the Table UIElement for displaying tabular data with optional headers and embedded widgets.
Supports custom column widths, row heights, alternating row backgrounds, and forwarding events to nested UIElements.
"""

import pygame
from typing import Any, List, Tuple

import setup.config as Config
from themes.theme_manager import get_color
from ui.components.base import UIElement
from ui.components.label import UILabel


class UITable(UIElement):
    """
    UI element that renders data in a grid layout.

    Features:
    - Optional header row with labels
    - Customizable column widths and row heights
    - Alternating row background colors for readability
    - Support for primitive data and UIElement cells
    - Automatic resizing based on content
    - Event propagation and update for embedded UIElements
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
        Initialize a Table instance at the given position.

        Args:
            x (int): X-coordinate of top-left corner.
            y (int): Y-coordinate of top-left corner.
            column_widths (List[int]): List of widths for each column.
            row_height (int): Height of each row in pixels.
            headers (List[str], optional): Text for header cells; if provided, creates a header row.
            font_size (int, optional): Font size for cell text; falls back to default if None.
            font_name (str, optional): Font family name for cell text; falls back to default if None.
        """
        # Compute initial dimensions: total width and height for header row if present
        total_width = sum(column_widths)
        initial_rows = 1 if headers else 0
        initial_height = initial_rows * row_height
        super().__init__(x, y, total_width, initial_height)

        self.column_widths = column_widths
        self.row_height = row_height
        self.headers = headers or []
        self.rows: List[List[Any]] = []

        # Determine font settings
        self.font_name = font_name or Config.fonts['default']['name']
        self.font_size = font_size or Config.fonts['default']['size']

        # Create header label objects if headers provided
        self.header_labels: List[UILabel] = []
        if self.headers:
            self._create_header_labels()

    def _create_header_labels(self) -> None:
        """
        Generate Label objects for the header row and position them in columns.
        """
        self.header_labels.clear()
        dx = self.x
        for idx, text in enumerate(self.headers):
            # Create a label with padding inside the header cell
            lbl = UILabel(                
                x=dx + 5,
                y=self.y + 5,
                text=text,
                font_size=self.font_size,
                font_name=self.font_name
            )
            self.header_labels.append(lbl)
            dx += self.column_widths[idx]

    def add_row(self, values: List[Any]) -> None:
        """
        Append a new row of data or UIElements to the table.

        Args:
            values (List[Any]): Cell contents matching column count; each value
                                can be a primitive or a UIElement instance.

        Raises:
            ValueError: If number of values does not match number of columns.
        """
        if len(values) != len(self.column_widths):
            raise ValueError("Column count mismatch")
        # Add the row and adjust table height
        self.rows.append(values)
        total_rows = len(self.rows) + (1 if self.headers else 0)
        self.height = total_rows * self.row_height
        self.rect.height = self.height

    def clear(self) -> None:
        """
        Remove all data rows while preserving header row.
        """
        self.rows.clear()
        self.height = (1 if self.headers else 0) * self.row_height
        self.rect.height = self.height

    def draw(self, surface: pygame.Surface) -> None:
        """
        Render the table: draw header row, alternating data rows, and embedded widgets or text.

        Args:
            surface (pygame.Surface): Target surface for rendering.
        """
        border_w = Config.ui['default']['border_width']

        # Draw header background and border
        if self.headers:
            hdr_rect = pygame.Rect(self.x, self.y, self.width, self.row_height)
            pygame.draw.rect(surface, get_color('panel_bg'), hdr_rect)
            pygame.draw.rect(surface, get_color('border'), hdr_rect, border_w)
            for lbl in self.header_labels:
                lbl.draw(surface)

        # Draw each data row with alternating backgrounds
        for ridx, row in enumerate(self.rows):
            y_off = self.y + (ridx + (1 if self.headers else 0)) * self.row_height
            dx = self.x
            for cidx, cell in enumerate(row):
                col_w = self.column_widths[cidx]
                cell_rect = pygame.Rect(dx, y_off, col_w, self.row_height)
                # Alternate background color for readability
                bg_key = 'background' if ridx % 2 == 0 else 'panel_bg'
                pygame.draw.rect(surface, get_color(bg_key), cell_rect)
                pygame.draw.rect(surface, get_color('border'), cell_rect, border_w)

                # Draw cell content: UIElement or text
                if isinstance(cell, UIElement):
                    cell.set_position(dx + 5, y_off + 5)
                    cell.draw(surface)
                else:
                    # Render primitive value as a Label
                    text_lbl = UILabel(                        
                        x=dx + 5,
                        y=y_off + 5,
                        text=str(cell),
                        font_size=self.font_size,
                        font_name=self.font_name
                    )
                    text_lbl.draw(surface)

                dx += col_w

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Propagate events to any UIElement instances embedded in cells.

        Args:
            event (pygame.event.Event): The event to dispatch.
        """
        for row in self.rows:
            for cell in row:
                if isinstance(cell, UIElement):
                    cell.handle_event(event)

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Update any interactive UIElement cells (e.g., hover states).

        Args:
            mouse_pos (Tuple[int,int]): Current mouse coordinates.
        """
        for row in self.rows:
            for cell in row:
                if isinstance(cell, UIElement):
                    cell.update(mouse_pos)
