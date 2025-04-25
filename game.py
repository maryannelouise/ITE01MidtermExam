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
    def __init__(self, level, mode):
        self.level = level
        self.rows = level.rows
        self.cols = level.cols
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
        self.background_color = (255, 255, 255) if mode == "Light" else (0, 0, 0)
        self.text_color = (0, 0, 0) if mode == "Light" else (255, 255, 255)
        self.flip_sound = pygame.mixer.Sound(os.path.join('sounds', 'flip.mp3'))
        self.match_sound = pygame.mixer.Sound(os.path.join('sounds', 'match.mp3'))
        self.no_match_sound = pygame.mixer.Sound(os.path.join('sounds', 'failed.mp3'))
        self.back_image = os.path.abspath(f"images/card/card_{self.level.difficulty[0]}.png")
        if not os.path.exists(self.back_image):
            self.back_image = os.path.abspath("images/card/card.png")
            if not os.path.exists(self.back_image):
                raise FileNotFoundError("No card back image found in images/card/")
        self.current_level_text = f"Level: {self.level.number}"
        try:
            self.set_card_size()
            self.generate_cards()
        except FileNotFoundError as e:
            print(f"Error loading game assets: {e}")
            self.create_default_cards()
        button_width = 200
        button_height = 50
        button_spacing = 20
        screen_width = pygame.display.get_surface().get_width()
        self.menu_button_rect = pygame.Rect(
            screen_width - button_width - button_spacing, 
            10, 
            button_width, 
            button_height
        )
        self.close_button_rect = pygame.Rect(
            screen_width - (2 * button_width) - (2 * button_spacing),
            10,
            button_width,
            button_height
        )
        self.go_back_button_rect = pygame.Rect(400, 450, 200, 50)

    def set_card_size(self):
        screen = pygame.display.get_surface()
        screen_width, screen_height = screen.get_size()
        grid_width = screen_width * 0.8
        grid_height = screen_height * 0.8
        max_card_width = grid_width // self.cols
        max_card_height = grid_height // self.rows
        self.width = min(200, max_card_width - 10)  
        self.height = min(280, max_card_height - 10) 

    def generate_cards(self):
        folder_path = os.path.abspath(os.path.join("images", self.level.difficulty, f"level{self.level.number}_{self.level.difficulty[0]}"))
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
        if self.game_over:
            button_width = 350  
            button_height = 50
            gap = 40 
            total_width = button_width * 2 + gap
            start_x = (self.screen.get_width() - total_width) // 2
            y_pos = self.screen.get_height()//2 + 50

            menu_rect = pygame.Rect(start_x, y_pos, button_width, button_height)
            close_rect = pygame.Rect(start_x + button_width + gap, y_pos, button_width, button_height)
            
            if menu_rect.collidepoint(pos):
                pygame.quit()
                os.system("python main.py")
                exit()
            elif close_rect.collidepoint(pos):
                pygame.quit()
                exit()
            return
        if not self.can_click or self.second_card is not None:
            return
        if self.close_button_rect.collidepoint(pos):
            pygame.quit()
            exit()
        if self.menu_button_rect.collidepoint(pos):
            return "menu"
        for card in self.cards:
            if (card.x <= pos[0] <= card.x + card.width and card.y <= pos[1] <= card.y + card.height and not card.revealed and not card.matched):
                card.flip()
                pygame.mixer.Sound.play(self.flip_sound)
                if self.first_card is None:
                    self.first_card = card
                elif self.second_card is None:
                    self.second_card = card
                    self.moves += 1
                    self.can_click = False
                    pygame.time.set_timer(pygame.USEREVENT, 1000)
                break
        self.current_level_text = f"Level: {self.level.number}"

    def check_match(self):
        if self.first_card and self.second_card:
            if self.first_card.image_path == self.second_card.image_path:
                self.first_card.matched = True
                self.second_card.matched = True
                pygame.mixer.Sound.play(self.match_sound)
                self.score += 10
            else:
                pygame.mixer.Sound.play(self.no_match_sound)
                self.first_card.flip()
                self.second_card.flip()
                self.score -= 1
        self.first_card = None
        self.second_card = None
        self.can_click = True

    def draw(self, screen):
        self.screen = screen
        screen.fill(self.background_color)
        for card in self.cards:
            card.draw(screen)
        elapsed_time = int(time.time() - self.start_time)
        timer_text = self.font.render(f"Time: {elapsed_time}s", True, self.text_color)
        screen.blit(timer_text, (10, 10))
        moves_text = self.font.render(f"Moves: {self.moves}", True, self.text_color)
        screen.blit(moves_text, (10, 60))
        score_text = self.font.render(f"Score: {self.score}", True, self.text_color)
        screen.blit(score_text, (10, 110))
        level_text = self.font.render(f"Level: {self.level.number}", True, self.text_color)
        screen.blit(level_text, (10, 160))
        pygame.draw.rect(screen, (200, 0, 0), self.close_button_rect)
        close_text = self.font.render("Close", True, self.text_color)
        screen.blit(close_text, (
            self.close_button_rect.centerx - close_text.get_width() // 2,
            self.close_button_rect.centery - close_text.get_height() // 2
        ))
        pygame.draw.rect(screen, (0, 0, 200), self.menu_button_rect)
        menu_text = self.font.render("Menu", True, self.text_color)
        screen.blit(menu_text, (
            self.menu_button_rect.centerx - menu_text.get_width() // 2,
            self.menu_button_rect.centery - menu_text.get_height() // 2
        ))

        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, (255, 0, 0) if self.mode == "Light" else (255, 100, 100))
            score_text = self.font.render(f"Final Score: {self.score}", True, self.text_color)
            game_over_rect = game_over_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 50))
            score_rect = score_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
            screen.blit(game_over_text, game_over_rect)
            screen.blit(score_text, score_rect)

            button_width = 350  
            button_height = 100
            gap = 40 
            
            total_width = button_width * 2 + gap
            start_x = (screen.get_width() - total_width) // 2
            y_pos = screen.get_height()//2 + 50

            menu_rect = pygame.Rect(start_x, y_pos, button_width, button_height)
            pygame.draw.rect(screen, (0, 100, 200), menu_rect, border_radius=20)
            menu_text = pygame.font.Font(None, 60).render("MENU", True, (255, 255, 255))
            screen.blit(menu_text, (menu_rect.centerx - menu_text.get_width()//2, menu_rect.centery - menu_text.get_height()//2))

            close_rect = pygame.Rect(start_x + button_width + gap, y_pos, button_width, button_height)
            pygame.draw.rect(screen, (200, 0, 0), close_rect, border_radius=20)
            close_text = pygame.font.Font(None, 60).render("CLOSE", True, (255, 255, 255))
            screen.blit(close_text, (close_rect.centerx - close_text.get_width()//2, close_rect.centery - close_text.get_height()//2))


    def update(self, event=None):
        if event and event.type == pygame.USEREVENT:
            self.check_match()
            pygame.time.set_timer(pygame.USEREVENT, 0)
        if all(card.matched for card in self.cards):
            self.game_over = True

    def reset(self, mode=None):
        self.flip_sound.stop()
        self.match_sound.stop()
        self.no_match_sound.stop()
        for card in self.cards:
            if card.image_path.startswith("temp_card_"):
                try:
                    os.remove(card.image_path)
                except:
                    pass
        mode_to_use = mode if mode is not None else self.mode
        return Game(self.level, mode_to_use)

    def resize(self):
        self.set_card_size()
        try:
            self.generate_cards()
        except FileNotFoundError:
            self.create_default_cards()

    def create_default_cards(self):
        self.cards.clear()
        colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), 
                  (255,0,255), (0,255,255), (255,128,0), (128,0,255)]
        for i in range(self.rows):
            for j in range(self.cols):
                pair_idx = (i * self.cols + j) % (len(colors)//2)
                color = colors[pair_idx]
                x = j * (self.width + 10) + self.x_offset
                y = i * (self.height + 10) + self.y_offset
                surf = pygame.Surface((self.width, self.height))
                surf.fill(color)
                pygame.draw.rect(surf, (0,0,0), (0,0,self.width,self.height), 2)
                temp_path = f"temp_card_{pair_idx}.png"
                pygame.image.save(surf, temp_path)
                self.cards.append(Card(temp_path, x, y, self.width, self.height, self.back_image))

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    pygame.display.set_caption("Memory Card Game")
    clock = pygame.time.Clock()
    running = True
    mode = "Dark"

    class Level:
        def __init__(self, difficulty, number, rows, cols):
            self.difficulty = difficulty
            self.number = number
            self.rows = rows
            self.cols = cols

    level = Level("easy", 1, 4, 4)
    game = Game(level, mode)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.handle_click(pygame.mouse.get_pos())
            elif event.type == pygame.USEREVENT:
                game.update(event)
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                game.resize()

        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()