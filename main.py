import pygame
import os
from game import Game
from display import Display
from level_selection import LevelSelection
from easy import EasyLevel
from medium import MediumLevel  # Import the MediumLevel class
from hard import HardLevel  # Import the HardLevel class

class Menu:
    def __init__(self, screen_width, screen_height):
        pygame.font.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.title_font = pygame.font.Font(None, int(screen_height * 0.08))
        self.option_font = pygame.font.Font(None, int(screen_height * 0.05))
        self.title = "Memory Match Game"
        
        self.option_texts = [
            "Easy (4x4)",
            "Medium (5x4)",
            "Hard (6x6)",
            "Light Mode",
            "Dark Mode",
            "Close"
        ]
        
        self.selected_mode = "Dark"
        self.hovered_option = None
        self.background_color = (20, 20, 20)
        self.text_color = (255, 255, 255)
        self.options = self.render_options()
    
    def render_options(self):
        colors = [
            (0, 255, 0),    # Green for Easy
            (255, 165, 0),  # Orange for Medium
            (255, 0, 0),    # Red for Hard
            self.text_color,
            self.text_color,
            self.text_color
        ]
        return [self.option_font.render(text, True, colors[i]) for i, text in enumerate(self.option_texts)]

    def draw(self, screen):
        self.draw_gradient_background(screen)
        
        title_surface = self.title_font.render(self.title, True, self.text_color)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height * 0.15))
        screen.blit(title_surface, title_rect)

        for i, option in enumerate(self.options):
            option_rect = option.get_rect(center=(self.screen_width // 2, self.screen_height * (0.3 + i * 0.1)))
            if self.hovered_option == i:
                pygame.draw.rect(screen, (100, 100, 100), option_rect.inflate(30, 20), border_radius=10)
                option = self.option_font.render(self.option_texts[i], True, (255, 215, 0))
            else:
                pygame.draw.rect(screen, (50, 50, 50) if self.selected_mode == "Dark" else (220, 220, 220), option_rect.inflate(30, 20), border_radius=10)
            screen.blit(option, option_rect)
    
    def draw_gradient_background(self, screen):
        base_color = (0, 0, 0) if self.selected_mode == "Dark" else (255, 255, 255)
        for y in range(self.screen_height):
            intensity = int(30 * (y / self.screen_height))
            r = max(0, min(255, base_color[0] + (intensity if self.selected_mode == "Light" else -intensity)))
            g = max(0, min(255, base_color[1] + (intensity if self.selected_mode == "Light" else -intensity)))
            b = max(0, min(255, base_color[2] + (intensity if self.selected_mode == "Light" else -intensity)))
            pygame.draw.line(screen, (r, g, b), (0, y), (self.screen_width, y))

    def handle_click(self, pos):
        for i in range(len(self.options)):
            option_rect = self.options[i].get_rect(center=(self.screen_width // 2, self.screen_height * (0.3 + i * 0.1)))
            if option_rect.collidepoint(pos):
                if i in [0, 1, 2]:  # Easy, Medium, Hard
                    return i + 1
                elif i == 3:
                    self.selected_mode = "Light"
                    self.background_color = (255, 255, 255)
                    self.text_color = (0, 0, 0)
                elif i == 4:
                    self.selected_mode = "Dark"
                    self.background_color = (20, 20, 20)
                    self.text_color = (255, 255, 255)
                elif i == 5:
                    pygame.quit()
                    exit()
                self.options = self.render_options()
                break
        return None

    def update_hover(self, pos):
        self.hovered_option = None
        for i in range(len(self.options)):
            option_rect = self.options[i].get_rect(center=(self.screen_width // 2, self.screen_height * (0.3 + i * 0.1)))
            if option_rect.collidepoint(pos):
                self.hovered_option = i
                break

def main():
    pygame.init()
    screen_info = pygame.display.Info()
    width, height = screen_info.current_w, screen_info.current_h

    display = Display(width, height, fullscreen=True)  

    game = None
    menu = Menu(width, height)
    level_selection = None
    easy_levels = EasyLevel()
    medium_levels = MediumLevel()  # Create an instance of MediumLevel
    hard_levels = HardLevel()  # Create an instance of HardLevel
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game:
                    if game.game_over:
                        game = game.reset(menu.selected_mode)
                    else:
                        game.handle_click(pygame.mouse.get_pos())
                elif level_selection:
                    level_number = level_selection.handle_click(pygame.mouse.get_pos())
                    if level_number:
                        if level_selection.title.startswith("Select Level - Easy"):
                            level = easy_levels.get_level(level_number)
                        elif level_selection.title.startswith("Select Level - Medium"):
                            level = medium_levels.get_level(level_number)
                        elif level_selection.title.startswith("Select Level - Hard"):  # Add this line
                            level = hard_levels.get_level(level_number)  # Add this line
                        game = Game(level, menu.selected_mode)
                        level_selection = None
                else:
                    difficulty = menu.handle_click(pygame.mouse.get_pos())
                    if difficulty:
                        if difficulty == 1:  # Easy
                            level_selection = LevelSelection(width, height, "Easy")
                        elif difficulty == 2:  # Medium
                            level_selection = LevelSelection(width, height, "Medium")
                        elif difficulty == 3:  # Hard
                            level_selection = LevelSelection(width, height, "Hard")  # Add this line

            elif event.type == pygame.MOUSEMOTION:
                if level_selection:
                    level_selection.update_hover(pygame.mouse.get_pos())
                else:
                    menu.update_hover(pygame.mouse.get_pos())

        display.clear()
        if game:
            game.update(event)  # Pass the event to the update method
            game.draw(display.screen)
        elif level_selection:
            level_selection.draw(display.screen)
        else:
            menu.draw(display.screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()