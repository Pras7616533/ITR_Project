import pygame
import sys
from game_logic import Game
from config import WIDTH, HEIGHT
from auth.auth_utils import logout_user

def main():
    # Initialize all imported pygame modules
    pygame.init()
    # Set up the display window with specified width and height
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # Set the window caption
    pygame.display.set_caption("Mystic Maze: The Quest for the Crystal")
    # Create a clock object to manage the frame rate
    clock = pygame.time.Clock()

    # Create an instance of the Game class
    game = Game(screen)

    running = True
    while running:
        # Event loop to process user input and system events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit the game loop if the window is closed
                running = False

            # Logout and restart the game if ESC key is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                logout_user()              # Call logout function
                main()                     # Restart the main function (game flow)
                return                     # Exit current main function

            # Pass the event to the game's event handler
            game.handle_event(event)

        # Update the game state
        game.update()
        # Update the full display surface to the screen
        pygame.display.flip()
        # Limit the frame rate to 60 frames per second
        clock.tick(60)

    # Quit pygame and exit the program
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
