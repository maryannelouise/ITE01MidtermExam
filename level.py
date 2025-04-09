class Level:
    def __init__(self, rows, cols, design, difficulty, number):
        self.rows = rows
        self.cols = cols
        self.design = design
        self.difficulty = difficulty
        self.number = number

    def __str__(self):
        return f"Level {self.number} ({self.difficulty}): {self.rows}x{self.cols} grid"
