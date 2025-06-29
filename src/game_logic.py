import csv
import time
import pygame
import pygame.time
import config
import sys

import resources
import pathfinder
from login_screen import LoginScreen
from text_input import TextInputBox
from maze_generator import generate_maze
from auth.auth_utils import auth_save_score, USER_FILE
from game_state import GameState
from button import Button, ImageButton
from leaderboard import load_leaderboard, save_score

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = GameState.LOGIN
        self.font = pygame.font.SysFont(None, 32)
        self.images = resources.load_assets_image()
        self.sounds = resources.load_assets_sounds()
        self.login = LoginScreen(self.screen)
        self.start_button = ImageButton(
            config.WIDTH // 2 - 60, 150, 
            self.images["start"] 
        )
        self.quit_button = ImageButton(
            config.WIDTH // 2 - 60, 220, 
            self.images["quit"] 
        )
        self.help_button = ImageButton(
            config.WIDTH // 2 - 60, 290, 
            self.images["help"] 
        )
        self.leaderboard_button = ImageButton(
            config.WIDTH // 2 - 60, 360, 
            self.images["leader_board"] 
        )
        self.logout_button = Button(
            config.WIDTH // 2 - 60, config.HEIGHT // 2 + 210, 150, 50, "Logout",
            self.font, (120, 80, 255), (255, 255, 255), hover_color=(80, 60, 200)
        )
        self.admin_button = Button(
            config.WIDTH // 2 - 60, config.HEIGHT // 2 + 280, 150, 50, "Admin Panel",
            self.font, (200, 200, 0), (0, 0, 0), hover_color=(180, 180, 20)
        )

        self.reset_info = ""
        self.restart_pressed = False
        self.level_won_sound_played = False
        self.show_minimap = True
        self.key_len = 0
        self.score = 0
        self.show_hint_to_key = False
        self.hint_path_to_key = []
        self.start_time = time.time()
        self.name_input_box = TextInputBox(config.WIDTH // 2 - 100, config.HEIGHT // 2, 200, 40, self.font)
        self.reset_user_box = TextInputBox(config.WIDTH // 2 - 100, 180, 200, 40, self.font)
        self.reset_pass_box = TextInputBox(config.WIDTH // 2 - 100, 240, 200, 40, self.font)
        self.entered_name = ""
        self.name = ""
        self.wall_theme = config.theme_index["wall"]
        self.player_theme = config.theme_index["player"]
        self.strip_theme = config.theme_index["strip"]
        self.theme = {
            "wall": self.wall_theme,
            "player": self.player_theme,
            "strip": self.strip_theme
        }

    def handle_event(self, event):
        if self.state == GameState.HOME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.reset_game()
                elif event.key == pygame.K_q:
                    auth_save_score(self.current_user, self.score)
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.is_clicked(pygame.mouse.get_pos()):
                    self.reset_game()
                elif self.quit_button.is_clicked(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
                elif self.help_button.is_clicked(pygame.mouse.get_pos()):
                    self.state = GameState.HELP
                elif self.leaderboard_button.is_clicked(pygame.mouse.get_pos()):
                    self.state = GameState.LEADERBOARD
                elif self.logout_button.is_clicked(pygame.mouse.get_pos()):
                    self.state = GameState.LOGOUT
            if config.logged_in_user == "admin" and self.admin_button.is_clicked(pygame.mouse.get_pos()):
                self.state = GameState.ADMIN

        elif self.state == GameState.RESET_PASSWORD:
            self.reset_user_box.handle_event(event)
            self.reset_pass_box.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    success = self.reset_password(self.reset_user_box.text, self.reset_pass_box.text)
                    if success:
                        self.reset_info = "Password updated successfully. Press B."
                    else:
                        self.reset_info = "User not found. Try again."
                elif event.key == pygame.K_b:
                    self.state = GameState.HOME

        elif self.state == GameState.ADMIN:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                self.state = GameState.HOME

        elif self.state == GameState.COMPLETED:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = GameState.HOME
                
        elif self.state == GameState.PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    self.show_hint_to_key = not self.show_hint_to_key
                elif event.key == pygame.K_m:
                    self.show_minimap = not self.show_minimap
                elif event.key == pygame.K_s:
                    self.change_theme("wall")
                    self.change_theme("strip")
                elif event.key == pygame.K_p:
                    self.change_theme("player")
                
        elif self.state == GameState.HELP:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                self.state = GameState.HOME
                
        elif self.state == GameState.LEADERBOARD:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                self.state = GameState.HOME

        elif self.state == GameState.NAME_INPUT:
            self.name = self.name_input_box.handle_event(event)
            if self.name:
                save_score(self.name, self.score)
                self.state = GameState.LEADERBOARD
                
        elif self.state == GameState.LOGOUT:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                config.logged_in_user = None
                self.state = GameState.LOGIN
            
        if self.state in [GameState.WON, GameState.LOST]:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and not self.restart_pressed:
                config.level = 1
                self.reset_game()
                self.restart_pressed = True
            if event.type == pygame.KEYUP and event.key == pygame.K_r:
                self.restart_pressed = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    def draw_minimap(self, surface, maze, scale=5):
        path_to_crystal = pathfinder.find_path_to_crystal()

        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                color = (50, 50, 50)
                if cell == 'P':
                    color = (0, 255, 0)
                elif cell == 'C':
                    color = (255, 255, 0)
                elif cell == 'K':
                    color = (0, 0, 255)
                elif cell == 'T':
                    color = (255, 0, 0)
                elif cell == 'H':
                    color = (0, 255, 255)
                elif cell == ' ':
                    color = (30, 30, 30)

                pygame.draw.rect(surface, color, (x * scale, y * scale, scale, scale))

        # Draw path to crystal as a dotted white trail
        for (x, y) in path_to_crystal:
            pygame.draw.rect(surface, (255, 255, 255), (x * scale + 1, y * scale + 1, scale - 2, scale - 2))

    def update(self):
        self.screen.fill((0, 0, 0))

        if self.state == GameState.HOME:
            self.screen.blit(self.images["bg"], (0, 0))
            title_text = self.font.render("🌀 Mystic Maze: The Quest for the Crystal", True, (255, 255, 255))
            self.screen.blit(title_text, (config.WIDTH // 6, config.HEIGHT // 3 + 30))
            self.start_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            self.leaderboard_button.draw(self.screen)
            self.help_button.draw(self.screen)
            self.logout_button.draw(self.screen)
            if config.logged_in_user == "admin":
                self.admin_button.draw(self.screen)

        if self.state == GameState.RESET_PASSWORD:
            self.screen.fill((25, 25, 25))
            title = self.font.render("🔐 Reset Password", True, (255, 255, 255))
            self.screen.blit(title, (config.WIDTH // 2 - 100, 100))

            self.reset_user_box.draw(self.screen)
            self.reset_pass_box.draw(self.screen)

            info = self.font.render("Press ENTER to reset, B to go back", True, (200, 200, 200))
            self.screen.blit(info, (config.WIDTH // 2 - 160, 300))
            if self.reset_info:
                info = self.font.render(self.reset_info, True, (0, 255, 0))
                self.screen.blit(info, (config.WIDTH // 2 - 140, 340))
           
        elif self.state == GameState.LEADERBOARD:
            self.screen.fill((20, 20, 50))
            title = self.font.render("🏆 Leaderboard - Top 10", True, (255, 255, 255))
            self.screen.blit(title, (config.WIDTH // 3, 50))
            
            scores = load_leaderboard()
            for i, entry in enumerate(scores):
                line = self.font.render(f"{i+1}. {entry['name']} - {entry['score']}", True, (255, 255, 0))
                self.screen.blit(line, (config.WIDTH // 3, 100 + i * 30))

            back_text = self.font.render("Press B to go back", True, (200, 200, 200))
            self.screen.blit(back_text, (config.WIDTH // 3, config.HEIGHT - 60))

        elif self.state == GameState.PLAYING:
            self.draw_element()
            self.collisions()

            # Timer logic
            elapsed = (pygame.time.get_ticks() - config.level_start_time) // 1000
            time_left = config.LEVEL_TIME_LIMIT - elapsed
            timer_text = self.font.render(f"⏱ Time Left: {time_left}s", True, (255, 255, 0))
            self.screen.blit(timer_text, (config.WIDTH - 200, 10))

            if time_left <= 0:
                self.state = GameState.LOST
            
            if self.show_minimap:
                minimap_surface = pygame.Surface((config.COLS * 5, config.ROWS * 5))
                self.draw_minimap(minimap_surface, self.maze, scale=5)
                self.screen.blit(minimap_surface, (config.WIDTH - 110, config.HEIGHT - 110))

        elif self.state == GameState.TRANSITION:
            elapsed = pygame.time.get_ticks() - config.transition_start_time
            countdown_left = max(0, config.COUNTDOWN_DURATION - elapsed)
            countdown_seconds = countdown_left // 1000 + 1  # +1 for intuitive countdown

            # Fill background
            self.screen.fill((0, 0, 0))

            # Display "Level X - Get Ready"
            level_text = self.font.render(f"Level {config.level} - Get Ready!", True, (255, 255, 255))
            self.screen.blit(level_text, (config.WIDTH // 3, config.HEIGHT // 2 - 50))

            # Show countdown and play sound
            self.sounds["countdown"].play()
            countdown_text = self.font.render(str(countdown_seconds), True, (255, 255, 0))
            self.screen.blit(countdown_text, (config.WIDTH // 2, config.HEIGHT // 2 + 20))

            # After countdown, start the game
            if elapsed >= config.COUNTDOWN_DURATION:
                self.state = GameState.PLAYING
                
        elif self.state == GameState.COMPLETED:
            text = self.font.render("All levels complete! Thanks for playing!", True, (0, 0, 255))
            self.screen.blit(text, (config.WIDTH // 6, config.HEIGHT // 2))
            text = self.font.render(f"Score: {self.score}", True, (0,150,150))
            self.screen.blit(text, (config.WIDTH // 2 - 60, config.HEIGHT // 2 + 30))

        elif self.state == GameState.LOST:
            lost_text = self.font.render("Game Over! Press R to Restart", True, (200, 0, 0))
            self.screen.blit(lost_text, (config.WIDTH // 4, config.HEIGHT // 2))
            self.sounds["losing"].play()
            self.score = 0
            
        elif self.state == GameState.LEVEL_WON:
            self.screen.fill((0, 0, 0))

            elapsed = pygame.time.get_ticks() - config.level_time
            
            # Display level complete text
            level_text = self.font.render(f"Level {config.level} complete!", True, (0, 105, 255))
            self.screen.blit(level_text, (config.WIDTH // 3, config.HEIGHT // 2 - 50))

            text = self.font.render(f"Score: {self.score}", True, (100,255,100))
            self.screen.blit(text, (config.WIDTH // 2 - 60, config.HEIGHT // 2 + 30))

            # Play level complete sound only once
            if not self.level_won_sound_played:
                self.sounds["level_complete"].play()
                self.level_won_sound_played = True

            # After countdown, either go to next level or complete game
            if elapsed >= config.LEVEL_COMPLETE_TIME:
                self.level_won_sound_played = False
                config.level += 1
                if config.level > config.MAX_LEVEL:
                    if not self.name:
                        self.state = GameState.NAME_INPUT
                    else:
                        self.state = GameState.COMPLETED
                else:
                    self.reset_game()
                    
        elif self.state == GameState.NAME_INPUT:
            self.screen.fill((0, 0, 0))
            prompt = self.font.render("Enter your name:", True, (255, 255, 255))
            self.screen.blit(prompt, (config.WIDTH // 2 - 100, config.HEIGHT // 2 - 50))
            self.name_input_box.draw(self.screen)
            if self.name:
                self.state = GameState.COMPLETED

        elif self.state == GameState.LOGOUT:
            self.screen.fill((30, 30, 30))
            text = self.font.render("You have been logged out.", True, (255, 255, 255))
            info = self.font.render("Press B to go back to Login Screen.", True, (180, 180, 180))
            if config.logged_in_user:
                user_text = self.font.render(f"Player: {config.logged_in_user}", True, (255, 255, 255))
                self.screen.blit(user_text, (20, 50))
            self.screen.blit(text, (config.WIDTH // 4, config.HEIGHT // 3))
            self.screen.blit(info, (config.WIDTH // 4, config.HEIGHT // 3 + 40))
        
        elif self.state == GameState.LOGIN:
            self.current_user = self.login.run()
            self.state = GameState.HOME
                       
        elif self.state == GameState.HELP:
            self.screen.fill((10, 10, 30))
            lines = [
                "Game Controls:",
                "- Arrow Keys: Move Player",
                "- Collect all keys 🗝️ to unlock the crystal 💎",
                "- Avoid traps ☠️, pick hearts ❤️ to heal",
                "- Press R: Restart on Game Over",
                "- Press M: Toggle Mini-map 🗺️",
                "- Press H: Toggle Hint to Nearest Key",
                "- Press B: Back to Home"
            ]
            for idx, line in enumerate(lines):
                text = self.font.render(line, True, (255, 255, 255))
                self.screen.blit(text, (50, 100 + idx * 40))

        elif self.state == GameState.ADMIN:
            self.screen.fill((10, 10, 40))
            title = self.font.render("Admin Panel - User Stats", True, (255, 255, 255))
            self.screen.blit(title, (config.WIDTH // 3, 40))

            stats = load_user_stats()
            for i, (username, score) in enumerate(stats[:10]):  # Top 10
                line = self.font.render(f"{i+1}. {username} - {score}", True, (200, 200, 200))
                self.screen.blit(line, (100, 100 + i * 35))

            back_text = self.font.render("Press B to return to Home", True, (180, 180, 180))
            self.screen.blit(back_text, (100, config.HEIGHT - 50))

    def draw_element(self):
        # Draw maze elements
            for x, y in config.walls: self.screen.blit(self.images["wall"][str(self.theme["wall"])], (x * config.TILE_SIZE, y * config.TILE_SIZE))
            for x, y in config.strips: self.screen.blit(self.images["strip"][str(self.theme["strip"])], (x * config.TILE_SIZE, y * config.TILE_SIZE))
            for x, y in config.keys: self.screen.blit(self.images["key"], (x * config.TILE_SIZE, y * config.TILE_SIZE))
            for x, y in config.traps: self.screen.blit(self.images["trap"], (x * config.TILE_SIZE, y * config.TILE_SIZE))
            for x, y in config.healths: self.screen.blit(self.images["heart"], (x * config.TILE_SIZE, y * config.TILE_SIZE))
            if config.crystal: self.screen.blit(self.images["crystal"], (config.crystal[0] * config.TILE_SIZE, config.crystal[1] * config.TILE_SIZE))
            self.screen.blit(self.images["player"][str(self.theme["player"])], (config.player_pos[0] * config.TILE_SIZE, config.player_pos[1] * config.TILE_SIZE))

            # HUD
            for i in range(config.health):
                self.screen.blit(self.images["heart"], (10 + i * 35, config.HEIGHT - 40))
            for i in range(config.collected_keys):
                self.screen.blit(self.images["key_icon"], (150 + i * 35, config.HEIGHT - 40))
            if config.crystal_found:
                self.screen.blit(self.images["crystal_icon"], (300, config.HEIGHT - 40))
            elapsed_time = int(time.time() - self.start_time)
            score_text = self.font.render(f"Score: {self.score}  Time: {elapsed_time}s", True, (255, 255, 255))
            self.screen.blit(score_text, (20, 20))

            if self.show_hint_to_key:
                self.hint_path_to_key = pathfinder.find_path_to_nearest_key()
                
            if self.show_hint_to_key and self.hint_path_to_key:
                for x, y in self.hint_path_to_key:
                    pygame.draw.rect(
                        self.screen, 
                        (0, 255, 0, 128), 
                        (x * config.TILE_SIZE + 10, y * config.TILE_SIZE + 10, 10, 10)
                    )

            # Handle keys
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_LEFT]: self.move(-1, 0); pygame.time.wait(150)
            if keys_pressed[pygame.K_RIGHT]: self.move(1, 0); pygame.time.wait(150)
            if keys_pressed[pygame.K_UP]: self.move(0, -1); pygame.time.wait(150)
            if keys_pressed[pygame.K_DOWN]: self.move(0, 1); pygame.time.wait(150)

    def collisions(self):
        if tuple(config.player_pos) in config.traps:
            config.traps.remove(tuple(config.player_pos))
            self.sounds["trap"].play()
            config.health -= 1
            self.score = max(0, self.score - 75)  # Penalty
            pygame.time.wait(300)
            if config.health <= 0:
                self.state = GameState.LOST

        if tuple(config.player_pos) in config.healths:
            config.healths.remove(tuple(config.player_pos))
            self.sounds["health"].play()
            config.health += 1
            self.score += 50
            pygame.time.wait(300)

        for k in config.keys[:]:
            if tuple(config.player_pos) == k:
                config.keys.remove(k)
                self.sounds["get_key"].play()
                config.collected_keys += 1
                self.score += 100

        if tuple(config.player_pos) == config.crystal and config.collected_keys >= self.key_len:
            self.score += 200
            elapsed = (pygame.time.get_ticks() - config.level_start_time) // 1000
            time_bonus = max(0, config.LEVEL_TIME_LIMIT - elapsed)
            self.score += time_bonus
            if config.logged_in_user:
                update_user_high_score(config.logged_in_user, self.score)
            self.state = GameState.LEVEL_WON
            config.level_time = pygame.time.get_ticks()
                            
    def reset_game(self):
        self.maze = generate_maze(config.ROWS, config.COLS, config.level)
        config.ROWS = min(15 + config.level, config.MAX_ROWS)
        config.COLS = min(20 + config.level, config.MAX_COLS)


        config.walls, config.keys, config.traps, config.healths, config.strips = [], [], [], [], []
        config.crystal, config.collected_keys, config.health, config.crystal_found = None, 0, 3, False
        config.transition_start_time = pygame.time.get_ticks()
        config.level_time = pygame.time.get_ticks()
        config.level_start_time = pygame.time.get_ticks()
        self.state = GameState.TRANSITION

        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == 'W': config.walls.append((x, y))
                elif cell == 'K': 
                    config.keys.append((x, y))
                    config.strips.append((x, y))
                elif cell == 'T': 
                    config.traps.append((x, y))
                    config.strips.append((x, y))
                elif cell == 'C': 
                    config.crystal = (x, y)
                    config.strips.append((x, y))
                elif cell == 'P': 
                    config.player_pos = [x, y]
                    config.strips.append((x, y))
                elif cell == 'H': 
                    config.healths.append((x, y))
                    config.strips.append((x, y))
                elif cell == ' ': config.strips.append((x, y))
                
        self.key_len = len(config.keys)        
        self.draw_minimap(self.screen, self.maze, scale=4)

    def move(self, dx, dy):
        new_x = config.player_pos[0] + dx
        new_y = config.player_pos[1] + dy
        if (new_x, new_y) not in config.walls:
            config.player_pos = [new_x, new_y]
            
    def change_theme(self, key: str):
        if config.theme_index[key] >= config.MAX_THEME:
            config.theme_index[key] = 0
        else:
            config.theme_index[key] += 1
        self.theme[key] = config.THEMES[key][config.theme_index[key]]

def load_user_stats():
    stats = []
    with open(USER_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            stats.append((row["username"], int(row.get("high_score", 0))))
    return sorted(stats, key=lambda x: x[1], reverse=True)

def update_user_high_score(username, score):
    import csv
    rows = []
    with open(USER_FILE, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["username"] == username:
                row["high_score"] = str(max(int(row.get("high_score", 0)), score))
            rows.append(row)
    with open(USER_FILE, "w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
