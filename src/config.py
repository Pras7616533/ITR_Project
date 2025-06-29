# Game config
TILE_SIZE = 50
ROWS, COLS = 10, 12
WIDTH, HEIGHT = COLS * TILE_SIZE + 50, ROWS * TILE_SIZE + 50
IMG_WIDTH, IMG_HEIGHT = 150, 65
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MAX_LEVEL = 1 # Max level
COUNTDOWN_DURATION = 4000  # 4 seconds in milliseconds
LEVEL_COMPLETE_TIME = 3000 # 3 seconds in milliseconds
MAX_ROWS = HEIGHT // TILE_SIZE
MAX_COLS = WIDTH // TILE_SIZE
LEVEL_TIME_LIMIT = 60  # seconds per level
THEMES = {
    "wall": ("0", "1", "2"),
    "player": ("0", "1", "2"),
    "strip": ("0", "1", "2")
}
MAX_THEME = 2

# Game variables (set in reset_game)
player_pos = [0, 0]
walls, keys, traps, healths, strips = [], [], [], [], []
crystal = None
collected_keys = 0
level_start_time = 0
level = 1
health = None
crystal_found = False
transition_start_time = None
level_time = None
theme_index = {
    "wall": 0,
    "player": 0,
    "strip": 0
}
theme = 0
logged_in_user = None
