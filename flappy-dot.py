import tkinter as tk
from gamelib import *

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

UPDATE_DELAY = 33

class FlappyDot(GameApp):
    def init_game(self):
        self.test_text = Text(self, "text", 200, 200)
        self.elements.append(self.test_text)

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(0, 0)

    app = FlappyDot(root, CANVAS_WIDTH, CANVAS_HEIGHT)
    root.mainloop()