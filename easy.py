import os
import pygame
from level import Level  

class EasyLevel:
    def __init__(self):
        self.levels = [
            {"rows": 4, "cols": 4, "design": "easy/level1_e"},
            {"rows": 4, "cols": 4, "design": "easy/level2_e"},
            {"rows": 4, "cols": 4, "design": "easy/level3_e"},
            {"rows": 4, "cols": 4, "design": "easy/level4_e"},
            {"rows": 4, "cols": 4, "design": "easy/level5_e"},
        ]

    def get_level(self, level_number):
        if 1 <= level_number <= len(self.levels):
            level_config = self.levels[level_number - 1]
            difficulty = "easy"  
            return Level(level_config["rows"], level_config["cols"], level_config["design"], difficulty, level_number)  
        else:
            raise ValueError("Invalid level number")