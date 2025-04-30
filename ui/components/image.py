# ui/components/image.py

"""
Defines UIImage UIElement for displaying images on screen.
Optionally supports scaling.
"""

import pygame
import logging
from ui.components.base import UIElement

logger = logging.getLogger(__name__)

class UIImage(UIElement):
    """
    UI Element for displaying an image.

    Attributes:
        image (pygame.Surface): The loaded image surface.
        scaled_image (pygame.Surface): Scaled version if width/height differ from original.
    """
    def __init__(
        self,
        x: int,
        y: int,
        image_path: str,
        width: int = None,
        height: int = None
    ) -> None:
        """
        Initialize a UIImage element.

        Args:
            x (int): X position.
            y (int): Y position.
            image_path (str): Path to the image file.
            width (int, optional): Desired width (scales if different from original).
            height (int, optional): Desired height (scales if different from original).
        """
        # Load the image
        try:
            image = pygame.image.load(image_path).convert_alpha()
        except Exception as e:
            logger.error(f"Failed to load image '{image_path}': {e}")
            image = pygame.Surface((10, 10))
            image.fill((255, 0, 0))  # fallback: red square

        # If width/height provided, scale image
        scaled_image = image
        if width and height:
            scaled_image = pygame.transform.smoothscale(image, (width, height))

        final_width, final_height = scaled_image.get_size()
        super().__init__(x, y, final_width, final_height)

        self.image = image
        self.scaled_image = scaled_image

        logger.debug(f"UIImage initialized at ({x},{y}) with size ({final_width},{final_height})")

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the image on the surface.

        Args:
            surface (pygame.Surface): The surface to draw on.
        """
        surface.blit(self.scaled_image, (self.x, self.y))

    def update(self, mouse_pos: tuple[int, int]) -> None:
        """
        Optionally implement hover behavior here later.
        """
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Optionally handle click events on image later.
        """
        pass
