import pygame

class Display:
    def __init__(self, width=None, height=None, fullscreen=False):
        pygame.init()
        info = pygame.display.Info()

        self.width = width if width else int(info.current_w * 0.8)
        self.height = height if height else int(info.current_h * 0.8)

        flags = pygame.RESIZABLE
        if fullscreen:
            flags |= pygame.FULLSCREEN
        
        self.screen = pygame.display.set_mode((self.width, self.height), flags)

    def clear(self, theme="dark"):
        """Clear screen with theme-appropriate color"""
        if theme.lower() == "dark":
            self.screen.fill((0, 0, 0))  
        else:
            self.screen.fill((255, 255, 255)) 

    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        if self.screen.get_flags() & pygame.FULLSCREEN:
            pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        else:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
