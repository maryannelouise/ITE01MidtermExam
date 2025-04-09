import os
import pygame
from level import Level  

class HardLevel:
    def __init__(self):
        self.levels = [
            {"rows": 6, "cols": 6, "design": "hard/level1_h"},
            {"rows": 6, "cols": 6, "design": "hard/level2_h"},
            {"rows": 6, "cols": 6, "design": "hard/level3_h"},
            {"rows": 6, "cols": 6, "design": "hard/level4_h"},
            {"rows": 6, "cols": 6, "design": "hard/level5_h"},
        ]

    def get_level(self, level_number):
        if 1 <= level_number <= len(self.levels):
            level_config = self.levels[level_number - 1]
            difficulty = "hard"  
            return Level(level_config["rows"], level_config["cols"], level_config["design"], difficulty, level_number)  
        else:
            raise ValueError("Invalid level number")