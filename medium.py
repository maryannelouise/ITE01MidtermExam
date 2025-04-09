import os
import pygame
from level import Level 

class MediumLevel:
    def __init__(self):
        self.levels = [
            {"rows": 5, "cols": 4, "design": "medium/level1_m"},
            {"rows": 5, "cols": 4, "design": "medium/level2_m"},
            {"rows": 5, "cols": 4, "design": "medium/level3_m"},
            {"rows": 5, "cols": 4, "design": "medium/level4_m"},
            {"rows": 5, "cols": 4, "design": "medium/level5_m"},
        ]

    def get_level(self, level_number):
        if 1 <= level_number <= len(self.levels):
            level_config = self.levels[level_number - 1]
            difficulty = "medium"  
            return Level(level_config["rows"], level_config["cols"], level_config["design"], difficulty, level_number)  
        else:
            raise ValueError("Invalid level number")