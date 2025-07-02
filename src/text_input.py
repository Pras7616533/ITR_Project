import pygame

class TextInputBox:
    def __init__(self, x, y, w, h, font, text=''):
        # Initialize the rectangle for the input box
        self.rect = pygame.Rect(x, y, w, h)
        # Define colors for active and inactive states
        self.color_inactive = pygame.Color('gray15')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive  # Start as inactive
        self.text = text  # Store the current text
        self.font = font  # Font used for rendering text
        # Render the initial text surface
        self.txt_surface = font.render(text, True, (255, 255, 255))
        self.active = False  # Track if the box is active (focused)

    def handle_event(self, event):
        # Handle mouse click events
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if the box is clicked
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive

        # Handle keyboard events when the box is active
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return self.text  # Return the input text on Enter
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]  # Remove last character
            else:
                # Limit input length to 12 characters
                if len(self.text) < 12:
                    self.text += event.unicode  # Add typed character
            # Re-render the text surface with updated text
            self.txt_surface = self.font.render(self.text, True, (255, 255, 255))
        return None  # No text to return

    def draw(self, screen):
        # Draw the text surface inside the input box
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Draw the rectangle border
        pygame.draw.rect(screen, self.color, self.rect, 2)
