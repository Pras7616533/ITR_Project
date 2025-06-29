import pygame
import sys
from auth.auth_utils import (
    get_remembered_user,
    init_user_file,
    remember_user,
    validate_user,
    register_user
)

class LoginScreen:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_size()
        self.font = pygame.font.SysFont(None, 32)
        self.clock = pygame.time.Clock()

        self.input_box_user = pygame.Rect(200, 100, 200, 40)
        self.input_box_pass = pygame.Rect(200, 160, 200, 40)
        self.login_btn = pygame.Rect(150, 230, 120, 40)
        self.signup_btn = pygame.Rect(310, 230, 120, 40)
        self.checkbox_rect = pygame.Rect(150, 275, 20, 20)

        self.user_text = ""
        self.pass_text = ""
        self.active_user = False
        self.active_pass = False
        self.remember_me = True
        self.error_msg = ""
        self.success_msg = ""

        init_user_file()

    def draw(self):
        self.screen.fill((30, 30, 30))

        title = self.font.render("🔐 Login / Sign Up", True, (255, 255, 255))
        self.screen.blit(title, (self.WIDTH // 2 - title.get_width() // 2, 30))

        pygame.draw.rect(self.screen, (50, 100, 255) if self.active_user else (200, 200, 200), self.input_box_user, 2)
        pygame.draw.rect(self.screen, (50, 100, 255) if self.active_pass else (200, 200, 200), self.input_box_pass, 2)

        user_surface = self.font.render(self.user_text, True, (255, 255, 255))
        pass_surface = self.font.render("*" * len(self.pass_text), True, (255, 255, 255))

        self.screen.blit(self.font.render("Username:", True, (255, 255, 255)), (100, 105))
        self.screen.blit(user_surface, (self.input_box_user.x + 10, self.input_box_user.y + 10))

        self.screen.blit(self.font.render("Password:", True, (255, 255, 255)), (100, 165))
        self.screen.blit(pass_surface, (self.input_box_pass.x + 10, self.input_box_pass.y + 10))

        pygame.draw.rect(self.screen, (50, 100, 255), self.login_btn)
        pygame.draw.rect(self.screen, (50, 100, 255), self.signup_btn)
        pygame.draw.rect(self.screen, (255, 255, 255), self.checkbox_rect, 2)

        self.screen.blit(self.font.render("Login", True, (255, 255, 255)), (self.login_btn.x + 30, self.login_btn.y + 10))
        self.screen.blit(self.font.render("Sign Up", True, (255, 255, 255)), (self.signup_btn.x + 20, self.signup_btn.y + 10))
        self.screen.blit(self.font.render("Remember Me", True, (255, 255, 255)), (180, 275))

        if self.remember_me:
            pygame.draw.rect(self.screen, (255, 255, 255), self.checkbox_rect.inflate(-4, -4))

        if self.error_msg:
            self.screen.blit(self.font.render(self.error_msg, True, (255, 0, 0)), (150, 310))
        if self.success_msg:
            self.screen.blit(self.font.render(self.success_msg, True, (0, 255, 0)), (150, 310))

        pygame.display.flip()

    def run(self):
        remembered = get_remembered_user()
        if remembered:
            return remembered  # Auto-login

        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.checkbox_rect.collidepoint(event.pos):
                        self.remember_me = not self.remember_me

                    self.active_user = self.input_box_user.collidepoint(event.pos)
                    self.active_pass = self.input_box_pass.collidepoint(event.pos)

                    if self.login_btn.collidepoint(event.pos):
                        if validate_user(self.user_text, self.pass_text):
                            self.success_msg = "Login successful!"
                            self.error_msg = ""
                            if self.remember_me:
                                remember_user(self.user_text)
                            pygame.time.wait(1000)
                            return self.user_text
                        else:
                            self.error_msg = "Invalid credentials."
                            self.success_msg = ""

                    if self.signup_btn.collidepoint(event.pos):
                        if register_user(self.user_text, self.pass_text):
                            self.success_msg = "Account created!"
                            self.error_msg = ""
                        else:
                            self.error_msg = "User already exists."
                            self.success_msg = ""

                if event.type == pygame.KEYDOWN:
                    if self.active_user:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            self.user_text += event.unicode
                    elif self.active_pass:
                        if event.key == pygame.K_BACKSPACE:
                            self.pass_text = self.pass_text[:-1]
                        else:
                            self.pass_text += event.unicode

            self.clock.tick(30)
