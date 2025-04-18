class UIManager:
    def __init__(self):
        self.elements = []

    def add(self, element):
        self.elements.append(element)

    def handle_event(self, event):
        for element in self.elements:
            if hasattr(element, "handle_event"):
                element.handle_event(event)

    def update(self, mouse_pos):
        for element in self.elements:
            if hasattr(element, "update"):
                element.update(mouse_pos)

    def draw(self, surface):
        for element in self.elements:
            if hasattr(element, "draw"):
                element.draw(surface)