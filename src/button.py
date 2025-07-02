from config import IMG_WIDTH, IMG_HEIGHT
import pygame

class ImageButton:
    def __init__(self, x, y, image):
        # Store the original image
        self.image = image
        # Create a slightly larger image for hover effect
        self.hover_image = pygame.transform.scale(image, (IMG_WIDTH + 10, IMG_HEIGHT + 10))
        # Set the position and size of the button
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        # Get current mouse position
        mouse_pos = pygame.mouse.get_pos()
        # If mouse is over the button, draw the hover image
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.hover_image, self.rect.topleft)
        else:
            # Otherwise, draw the normal image
            screen.blit(self.image, self.rect.topleft)

    def is_clicked(self, pos):
        # Check if the given position is inside the button's area
        return self.rect.collidepoint(pos)

class Button:
    def __init__(self, x, y, width, height, text, font, color, text_color, hover_color=None):
        # Create a rectangle for the button's area
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color
        # Use hover_color if provided, otherwise use the normal color
        self.hover_color = hover_color if hover_color else color

    def draw(self, screen):
        # Set the button color based on mouse hover
        current_color = self.color
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            current_color = self.hover_color

        # Draw the button rectangle with rounded corners
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)
        # Render the button text
        text_surf = self.font.render(self.text, True, self.text_color)
        # Center the text on the button
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos):
        # Check if the given mouse position is inside the button's area
        return self.rect.collidepoint(mouse_pos)
