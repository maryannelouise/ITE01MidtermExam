import os
import pygame

class Level:
    def __init__(self, rows, cols, design, difficulty, number):  # Add number parameter
        self.rows = rows
        self.cols = cols
        self.design = design
        self.difficulty = difficulty  # Store difficulty as an instance attribute
        self.number = number  # Store level number as an instance attribute
        self.cards = self.load_cards()

    def load_cards(self):
        base_path = os.path.dirname(os.path.abspath(__file__))  # Ensure absolute path
        image_folder = os.path.join(base_path, 'images', self.design)  # Use design only
        card_images = []

        if not os.path.exists(image_folder):
            print(f"❌ Error: Image folder '{image_folder}' not found!")
            return card_images  # Return empty list to prevent crashing

        # Adjust the folder structure based on difficulty
        if self.difficulty == "easy":
            image_folder = os.path.join(image_folder, f"level{self.number}_e")
        elif self.difficulty == "medium":
            image_folder = os.path.join(image_folder, f"level{self.number}_m")

        print(f"Looking for images in: {image_folder}")  # Debugging output

        if not os.path.exists(image_folder):
            print(f"❌ Error: Difficulty folder '{image_folder}' not found!")
            return card_images  # Return empty list to prevent crashing

        for filename in os.listdir(image_folder):
            if filename.endswith('.png'):
                image_path = os.path.join(image_folder, filename)
                try:
                    card_image = pygame.image.load(image_path)
                    card_images.append(card_image)
                except Exception as e:
                    print(f"⚠️ Error loading {filename}: {e}")

        return card_images

    def update(self):
        # Update level logic
        pass

    def draw(self, screen):
        # Draw cards and other elements
        pass

    def handle_click(self, pos):
        # Handle card clicks
        pass