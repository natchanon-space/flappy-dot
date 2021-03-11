import tkinter as tk
import random
from gamelib import *

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

UPDATE_DELAY = 33
PILLAR_SPEED = 5

class FlappyDot(GameApp):
    def init_game(self):
        # self.test_text = Text(self, "text", 200, 200)
        # self.elements.append(self.test_text)

        # self.circle = Contour(self, "c", x=100, y=100, size_x=100, size_y=100)
        # self.elements.append(self.circle)

        # self.rectangle = Contour(self, "r", x=400, y=400, size_x=100, size_y=100, color="red")
        # self.elements.append(self.rectangle)

        self.create_pillars()

    def create_pillars(self):
        rand_point = random.randint(50, self.canvas_height-50)
        space = 120
        width = self.canvas_width / 10

        upper_height = rand_point - space/2
        upper_y = upper_height/2

        lower_height = self.canvas_height - rand_point - space/2
        lower_y = self.canvas_height - lower_height/2

        self.upper_pillar = Contour(self, "r", color="blue", x=200, y=upper_y, size_x=width, size_y=upper_height)
        self.lower_pillar = Contour(self, "r", color="red", x=200, y=lower_y, size_x=width, size_y=lower_height)

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(0, 0)

    app = FlappyDot(root, CANVAS_WIDTH, CANVAS_HEIGHT)

    # print(app.circle.get_hitbox())
    # print(app.rectangle.get_hitbox())
    # print(app.test_text.text)

    root.mainloop()