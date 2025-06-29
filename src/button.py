from config import IMG_WIDTH, IMG_HEIGHT
import pygame

class ImageButton:
    def __init__(self, x, y, image):
        self.image = image
        self.hover_image = pygame.transform.scale(image, (IMG_WIDTH + 10, IMG_HEIGHT + 10))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.hover_image, self.rect.topleft)
        else:
            screen.blit(self.image, self.rect.topleft)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Button:
    def __init__(self, x, y, width, height, text, font, color, text_color, hover_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color
        self.hover_color = hover_color if hover_color else color

    def draw(self, screen):
        current_color = self.color
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            current_color = self.hover_color

        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
