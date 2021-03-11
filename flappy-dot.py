import tkinter as tk
import random
from gamelib import *

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

UPDATE_DELAY = 33
PILLAR_SPEED = 5

class FlappyDot(GameApp):
    def init_game(self):
        self.test_text = Text(self, "text", 200, 200)
        self.elements.append(self.test_text)

        self.circle = Contour(self, "c", x=100, y=100, size_x=100, size_y=100)
        self.elements.append(self.circle)

        self.rectangle = Contour(self, "r", x=400, y=400, size_x=100, size_y=100, color="red")
        self.elements.append(self.rectangle)

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(0, 0)

    app = FlappyDot(root, CANVAS_WIDTH, CANVAS_HEIGHT)

    print(app.circle.get_hitbox())
    print(app.rectangle.get_hitbox())
    print(app.test_text.text)

    root.mainloop()