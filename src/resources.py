from config import TILE_SIZE, WIDTH, HEIGHT, IMG_WIDTH, IMG_HEIGHT
import pygame
import os

# Choose the theme here
THEME_NAME = "image"  # Change to "dark", "forest", etc. if you add more themes
THEME_PATH = os.path.join("assets", THEME_NAME)

def load_image(path, size, colorkey=None):
    try:        
        image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)
        return image
    except pygame.error as e:
        print(f"Unable to load image at {path}: {e}")
        return None

def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except pygame.error as e:
        print(f"Unable to load sound at {path}: {e}")
        return None

def load_assets_image():
    images = {
        "wall": {
            "0": load_image(os.path.join(THEME_PATH, "wall", "0.png"), (TILE_SIZE, TILE_SIZE)),
            "1": load_image(os.path.join(THEME_PATH, "wall", "1.png"), (TILE_SIZE, TILE_SIZE)),
            "2": load_image(os.path.join(THEME_PATH, "wall", "2.png"), (TILE_SIZE, TILE_SIZE))
        },
        "player": {
            "0": load_image(os.path.join(THEME_PATH, "player", "0.png"), (TILE_SIZE, TILE_SIZE)),
            "1": load_image(os.path.join(THEME_PATH, "player", "1.png"), (TILE_SIZE, TILE_SIZE)),
            "2": load_image(os.path.join(THEME_PATH, "player", "2.png"), (TILE_SIZE, TILE_SIZE))
        },
        "strip": {
            "0": load_image(os.path.join(THEME_PATH, "strip", "0.png"), (TILE_SIZE, TILE_SIZE)),
            "1": load_image(os.path.join(THEME_PATH, "strip", "1.png"), (TILE_SIZE, TILE_SIZE)),
            "2": load_image(os.path.join(THEME_PATH, "strip", "2.png"), (TILE_SIZE, TILE_SIZE))
        },
        "key": load_image(os.path.join(THEME_PATH, "key.png"), (TILE_SIZE, TILE_SIZE)),
        "trap": load_image(os.path.join(THEME_PATH, "trap.png"), (TILE_SIZE, TILE_SIZE)),
        "heart": load_image(os.path.join(THEME_PATH, "heart.png"), (TILE_SIZE, TILE_SIZE)),
        "crystal": load_image(os.path.join(THEME_PATH, "crystal.png"), (TILE_SIZE, TILE_SIZE)),
        "bg": load_image(os.path.join(THEME_PATH, "bg.png"), (WIDTH, HEIGHT)),

        # Icons
        "heart_icon": load_image(os.path.join(THEME_PATH, "icons", "heart_icon.png"), (32, 32)),
        "key_icon": load_image(os.path.join(THEME_PATH, "icons", "key_icon.png"), (32, 32)),
        "crystal_icon": load_image(os.path.join(THEME_PATH, "icons", "crystal_icon.png"), (32, 32)),
        
        # Home icon
        "help" : load_image(os.path.join(THEME_PATH, "home", "help.png"), (IMG_WIDTH, IMG_HEIGHT)),
        "leader_board" : load_image(os.path.join(THEME_PATH, "home", "leader_board.png"), (IMG_WIDTH, IMG_HEIGHT)),
        "quit" : load_image(os.path.join(THEME_PATH, "home", "quit.png"), (IMG_WIDTH, IMG_HEIGHT)),
        "start" : load_image(os.path.join(THEME_PATH, "home", "start.png"), (IMG_WIDTH, IMG_HEIGHT)),
    }
    return images

def load_assets_sounds():
    sound_path = os.path.join("assets", "sound")
    sounds = {
        "trap": load_sound(os.path.join(sound_path, "trap.wav")),
        "health": load_sound(os.path.join(sound_path, "health_recharge.wav")),
        "get_key": load_sound(os.path.join(sound_path, "get_key.wav")),
        "level_complete": load_sound(os.path.join(sound_path, "level_complet.wav")),
        "losing": load_sound(os.path.join(sound_path, "losing.wav")),
        "countdown": load_sound(os.path.join(sound_path, "countdown.wav")),
    }
    return sounds
