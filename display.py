import pygame

class Display:
    def __init__(self, width=None, height=None, fullscreen=False):
        pygame.init()
        info = pygame.display.Info()

        # If width/height are not provided, default to 80% of the screen size
        self.width = width if width else int(info.current_w * 0.8)
        self.height = height if height else int(info.current_h * 0.8)

        flags = pygame.RESIZABLE
        if fullscreen:
            flags |= pygame.FULLSCREEN
        
        self.screen = pygame.display.set_mode((self.width, self.height), flags)

    def clear(self):
        self.screen.fill((0, 0, 0))  # Clear screen with black
