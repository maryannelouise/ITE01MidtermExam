# easy.py
import os
import pygame
from level import Level  # Assuming you have a Level class defined in level.py

class EasyLevel:
    def __init__(self):
        self.levels = [
            {"rows": 4, "cols": 4, "design": "easy/level1"},
            {"rows": 4, "cols": 4, "design": "easy/level2"},
            {"rows": 4, "cols": 4, "design": "easy/level3"},
            {"rows": 4, "cols": 4, "design": "easy/level4"},
            {"rows": 4, "cols": 4, "design": "easy/level5"},
        ]

    def get_level(self, level_number):
        if 1 <= level_number <= len(self.levels):
            level_config = self.levels[level_number - 1]
            difficulty = "easy"  # Define the difficulty level
            return Level(level_config["rows"], level_config["cols"], level_config["design"], difficulty, level_number)  # Pass level_number
        else:
            raise ValueError("Invalid level number")