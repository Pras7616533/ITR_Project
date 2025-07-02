# Game configuration constants
TILE_SIZE = 50  # Size of each tile in pixels
ROWS, COLS = 10, 12  # Number of rows and columns in the game grid
WIDTH, HEIGHT = COLS * TILE_SIZE + 50, ROWS * TILE_SIZE + 50  # Window size (with padding)
IMG_WIDTH, IMG_HEIGHT = 150, 65  # Image dimensions for UI elements
FPS = 60  # Frames per second (game speed)
WHITE = (255, 255, 255)  # RGB color for white
BLACK = (0, 0, 0)  # RGB color for black
MAX_LEVEL = 3  # Maximum number of levels in the game
COUNTDOWN_DURATION = 4000  # Countdown duration before level starts (milliseconds)
LEVEL_COMPLETE_TIME = 3000  # Time to show level complete screen (milliseconds)
MAX_ROWS = HEIGHT // TILE_SIZE  # Maximum rows based on window height
MAX_COLS = WIDTH // TILE_SIZE  # Maximum columns based on window width
LEVEL_TIME_LIMIT = 60  # Time limit per level in seconds

# Theme configuration for different game elements
THEMES = {
    "wall": ("0", "1", "2"),    # Theme indices for wall
    "player": ("0", "1", "2"),  # Theme indices for player
    "strip": ("0", "1", "2")    # Theme indices for strip
}
MAX_THEME = 2  # Maximum theme index

# Game variables (these are reset at the start of each game)
player_pos = [0, 0]  # Player's position on the grid
walls, keys, traps, healths, strips = [], [], [], [], []  # Lists for game objects
crystal = None  # Crystal object (goal)
collected_keys = 0  # Number of keys collected by the player
level_start_time = 0  # Time when the level started
level = 1  # Current level number
health = None  # Player's health
crystal_found = False  # Whether the crystal has been found
transition_start_time = None  # Time when level transition started
level_time = None  # Time spent in the current level

# Theme index for each element
theme_index = {
    "wall": 0,
    "player": 0,
    "strip": 0
}
theme = 0  # Current theme index
logged_in_user = None  # Username of the currently logged-in user
