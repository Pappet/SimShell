import random

# Color Codes for simpler use

# Use it with:
# Color.Black
# etc.

WHITE = (255, 255, 255)
LIGHT_GRAY = (211, 211, 211)
GRAY = (169, 169, 169)
DARK_GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

BROWN = (210, 105, 30)
PURPLE = (128, 0, 128)


def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)