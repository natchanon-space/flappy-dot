import tkinter as tk
from gamelib import *

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

UPDATE_DELAY = 33

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(0, 0)

    app = GameApp(root, CANVAS_WIDTH, CANVAS_HEIGHT)
    root.mainloop()