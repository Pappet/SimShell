# tests/test_button.py

import pytest
import pygame
from ui.components.button import Button
from core.config import FONT_NAME, FONT_SIZE

pygame.init()

def test_button_hover_and_click(tmp_path):
    # Erstelle Button und simuliere Mausbewegung / Klick
    btn = Button((0, 0, 50, 20), "OK", lambda: setattr(btn, "clicked", True))
    # Simuliere Hover
    btn.update((10, 10))
    assert btn.hovered is True

    # Simuliere Klick-Event
    mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(10,10))
    btn.handle_event(mock_event)
    assert getattr(btn, "clicked", False) is True
