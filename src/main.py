import pygame
import sys
from game_logic import Game
from config import WIDTH, HEIGHT
from login_screen import LoginScreen
from auth.auth_utils import logout_user

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mystic Maze: The Quest for the Crystal")
    clock = pygame.time.Clock()

    # Start Game
    game = Game(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Logout on ESC key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                logout_user()
                main()  # Restart main flow
                return

            game.handle_event(event)

        game.update()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
