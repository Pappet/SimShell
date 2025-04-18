import pytest
from core.events.event_handlers import update_energy_ui


class DummyBar:
    def __init__(self):
        self.value = None
    def set_value(self, value):
        self.value = value

class DummyLabel:
    def __init__(self):
        self.text = None
    def set_text(self, text):
        self.text = text


@pytest.mark.parametrize("input_val, expected_text", [
    (0, "Energie: 0"),
    (10.7, "Energie: 10"),
    (5.9, "Energie: 5"),
    (-3, "Energie: -3"),
])
def test_update_energy_ui_sets_bar_and_label(input_val, expected_text):
    bar = DummyBar()
    label = DummyLabel()
    update_energy_ui(input_val, bar, label)
    # Bar should receive exact value
    assert bar.value == input_val
    # Label text should reflect integer conversion
    assert label.text == expected_text
