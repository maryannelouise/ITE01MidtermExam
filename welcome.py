import pygame
import sys
import os

class WelcomePage:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.background_image = pygame.image.load(os.path.join("images", "MemoFLip.png"))
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        self.input_background_image = pygame.image.load(os.path.join("images", "WelcomeBg.png"))
        self.input_background_image = pygame.transform.scale(self.input_background_image, (self.screen_width, self.screen_height))
        self.font = pygame.font.Font(None, 50)
        self.input_font = pygame.font.Font(None, 40)
        self.clock = pygame.time.Clock()
        self.player_name = ""
        self.state = "start" 
        self.start_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2, 200, 50)
        self.start_button_rect = pygame.Rect(self.screen_width // 2 - 100, int(self.screen_height * 0.56), 200, 60)

    def draw_start(self):
        self.screen.blit(self.background_image, (0, 0))
        pygame.draw.rect(self.screen, (128, 0, 0), self.start_button_rect, border_radius=10)
        start_text = self.font.render("Start", True, (255, 255, 255))
        text_rect = start_text.get_rect(center=self.start_button_rect.center)
        self.screen.blit(start_text, text_rect)

    def draw_input_name(self):
        self.screen.blit(self.input_background_image, (0, 0))
        prompt_text = self.font.render("Enter your name:", True, (255, 255, 255))
        self.screen.blit(prompt_text, (self.screen_width // 2 - prompt_text.get_width() // 2, self.screen_height // 3))
        input_box = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 - 30, 300, 60)
        pygame.draw.rect(self.screen, (255, 255, 255), input_box, 2)
        name_text = self.input_font.render(self.player_name, True, (255, 255, 255))
        self.screen.blit(name_text, (input_box.x + 10, input_box.y + 10))

    def draw_welcome_message(self):
        self.screen.blit(self.input_background_image, (0, 0))
        welcome_text = self.font.render(f"Welcome, {self.player_name}!", True, (255, 255, 255))
        self.screen.blit(welcome_text, (self.screen_width // 2 - welcome_text.get_width() // 2, self.screen_height // 2 - 30))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.state == "start":
                        if self.start_button_rect.collidepoint(event.pos):
                            self.state = "input_name"
                elif event.type == pygame.KEYDOWN:
                    if self.state == "input_name":
                        if event.key == pygame.K_RETURN:
                            if self.player_name.strip() != "":
                                self.state = "welcome_message"
                                self.welcome_start_time = pygame.time.get_ticks()
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        else:
                            if len(self.player_name) < 20 and event.unicode.isprintable():
                                self.player_name += event.unicode

            if self.state == "start":
                self.draw_start()
            elif self.state == "input_name":
                self.draw_input_name()
            elif self.state == "welcome_message":
                self.draw_welcome_message()
                if pygame.time.get_ticks() - self.welcome_start_time > 2000:
                    running = False

            pygame.display.flip()
            self.clock.tick(60)
