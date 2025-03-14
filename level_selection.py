# level_selection.py
import pygame

class LevelSelection:
    def __init__(self, screen_width, screen_height, difficulty):
        pygame.font.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title_font = pygame.font.Font(None, int(screen_height * 0.08))
        self.option_font = pygame.font.Font(None, int(screen_height * 0.05))
        self.title = f"Select Level - {difficulty.capitalize()}"
        
        self.option_texts = [f"Level {i + 1}" for i in range(5)]
        self.hovered_option = None
        self.background_color = (20, 20, 20)
        self.text_color = (255, 255, 255)
        self.options = self.render_options()

    def render_options(self):
        return [self.option_font.render(text, True, self.text_color) for text in self.option_texts]

    def draw(self, screen):
        screen.fill(self.background_color)
        title_surface = self.title_font.render(self.title, True, self.text_color)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height * 0.15))
        screen.blit(title_surface, title_rect)

        for i, option in enumerate(self.options):
            option_rect = option.get_rect(center=(self.screen_width // 2, self.screen_height * (0.3 + i * 0.1)))
            if self.hovered_option == i:
                pygame.draw.rect(screen, (100, 100, 100), option_rect.inflate(30, 20), border_radius=10)
                option = self.option_font.render(self.option_texts[i], True, (255, 215, 0))  # Highlight color
            else:
                pygame.draw.rect(screen, (50, 50, 50), option_rect.inflate(30, 20), border_radius=10)
            screen.blit(option, option_rect)

    def handle_click(self, pos):
        for i in range(len(self.options)):
            option_rect = self.options[i].get_rect(center=(self.screen_width // 2, self.screen_height * (0.3 + i * 0.1)))
            if option_rect.collidepoint(pos):
                return i + 1  # Return level number (1-5)
        return None

    def update_hover(self, pos):
        self.hovered_option = None
        for i in range(len(self.options)):
            option_rect = self.options[i].get_rect(center=(self.screen_width // 2, self.screen_height * (0.3 + i * 0.1)))
            if option_rect.collidepoint(pos):
                self.hovered_option = i
                break