import pygame
import random
import time
import os

pygame.init()
pygame.mixer.init()

class Card:
    def __init__(self, image_path, x, y, width, height, back_image):
        self.image_path = image_path
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.back_image = pygame.image.load(back_image)
        self.back_image = pygame.transform.scale(self.back_image, (width, height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.revealed = False
        self.matched = False

    def draw(self, screen):
        screen.blit(self.image if self.revealed or self.matched else self.back_image, (self.x, self.y))

    def flip(self):
        self.revealed = not self.revealed

class Game:
    def __init__(self, rows=5, cols=4, level=None, mode="Dark"):
        self.rows = rows
        self.cols = cols
        self.cards = []
        self.first_card = None
        self.second_card = None
        self.can_click = True
        self.score = 0
        self.moves = 0
        self.start_time = time.time()
        self.font = pygame.font.Font(None, 48)
        self.game_over = False
        self.mode = mode
        self.level = level
        self.background_color = (255, 255, 255) if mode == "Light" else (0, 0, 0)
        self.text_color = (0, 0, 0) if mode == "Light" else (255, 255, 255)

        self.flip_sound = self.load_sound("flip.mp3")
        self.match_sound = self.load_sound("match.mp3")
        self.no_match_sound = self.load_sound("failed.mp3")
        self.back_image = os.path.join("images", "card", "card_m.png")

        self.set_card_size()
        self.generate_cards()

    def load_sound(self, filename):
        path = os.path.join("sounds", filename)
        if os.path.exists(path):
            return pygame.mixer.Sound(path)
        else:
            print(f"⚠️ Warning: Sound file '{filename}' not found.")
            return None

    def set_card_size(self):
        screen = pygame.display.get_surface()
        screen_width, screen_height = screen.get_size()
        
        grid_width = screen_width * 0.8
        grid_height = screen_height * 0.8
        
        max_card_width = grid_width // self.cols
        max_card_height = grid_height // self.rows

        self.width = min(150, max_card_width - 10)
        self.height = min(200, max_card_height - 10)

    def generate_cards(self):
        if not self.level:
            raise ValueError("❌ Error: Level information is missing!")

        # Ensure level difficulty and number are formatted correctly
        difficulty = self.level["difficulty"]
        level_number = self.level["number"]

        # Correct path handling
        folder_path = os.path.abspath(os.path.join("images", difficulty, f"level{level_number}_{difficulty[0]}"))

        # Debugging: Print the resolved folder path
        print(f"Resolved folder path: {folder_path}")

        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"❌ Error: Image folder '{folder_path}' not found!")

        images = [os.path.join(folder_path, f"{i}.png") for i in range(1, (self.rows * self.cols) // 2 + 1)]
        
        for img in images:
            if not os.path.exists(img):
                raise FileNotFoundError(f"❌ Error: Image '{img}' not found!")

        num_pairs = (self.rows * self.cols) // 2
        selected_images = random.sample(images, num_pairs) * 2
        random.shuffle(selected_images)

        screen = pygame.display.get_surface()
        screen_width, screen_height = screen.get_size()
        
        self.x_offset = (screen_width - (self.cols * (self.width + 10))) // 2
        self.y_offset = (screen_height - (self.rows * (self.height + 10))) // 2

        self.cards.clear()
        for i in range(self.rows):
            for j in range(self.cols):
                image = selected_images.pop()
                x = j * (self.width + 10) + self.x_offset
                y = i * (self.height + 10) + self.y_offset
                self.cards.append(Card(image, x, y, self.width, self.height, self.back_image))

    def handle_click(self, pos):
        if self.game_over or not self.can_click or self.second_card is not None:
            return

        for card in self.cards:
            if (card.x <= pos[0] <= card.x + card.width and card.y <= pos[1] <= card.y + card.height and not card.revealed and not card.matched):
                card.flip()
                if self.flip_sound:
                    pygame.mixer.Sound.play(self.flip_sound)

                if self.first_card is None:
                    self.first_card = card
                elif self.second_card is None:
                    self.second_card = card
                    self.moves += 1  
                    self.can_click = False  
                    pygame.time.set_timer(pygame.USEREVENT, 1000)  
                break

    def check_match(self):
        if self.first_card and self.second_card:
            if self.first_card.image_path == self.second_card.image_path:
                self.first_card.matched = True
                self.second_card.matched = True
                if self.match_sound:
                    pygame.mixer.Sound.play(self.match_sound)
                self.score += 10
            else:
                if self.no_match_sound:
                    pygame.mixer.Sound.play(self.no_match_sound)
                self.first_card.flip()
                self.second_card.flip()
                self.score = max(0, self.score - 1)
        
        self.first_card = None
        self.second_card = None
        self.can_click = True  

    def draw(self, screen):
        screen.fill(self.background_color)
        for card in self.cards:
            card.draw(screen)

        elapsed_time = int(time.time() - self.start_time)
        screen.blit(self.font.render(f"Time: {elapsed_time}s", True, self.text_color), (10, 10))
        screen.blit(self.font.render(f"Moves: {self.moves}", True, self.text_color), (10, 60))
        screen.blit(self.font.render(f"Score: {self.score}", True, self.text_color), (10, 110))

        if self.game_over:
            game_over_text = self.font.render("Game Over!", True, self.text_color)
            screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, screen.get_height() // 2))

    def update(self, event=None):  
        if event and event.type == pygame.USEREVENT:
            self.check_match()
            pygame.time.set_timer(pygame.USEREVENT, 0)  

        if all(card.matched for card in self.cards):
            self.game_over = True

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Memory Card Game - Medium Level")
    clock = pygame.time.Clock()
    running = True

    level_info = {"difficulty": "medium", "number": 1}
    game = Game(level=level_info)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.handle_click(pygame.mouse.get_pos())
            elif event.type == pygame.USEREVENT:
                game.update(event)

        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
