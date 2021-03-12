import tkinter as tk
from gamelib import GameApp, Contour

class Tester(GameApp):
    def init_game(self):
        self.dot = Contour(self, "images/dot.png", x=100, y=100)
        print("x:", self.dot.x, "y:", self.dot.y)

        print("img_width:", self.dot.photo_image.width(), "img_height:", self.dot.photo_image.height())
        hb = self.dot.get_hitbox()

        print("hitbix", hb)
        
        self.canvas.create_rectangle(hb[0], hb[1], hb[2], hb[3])

root = tk.Tk()
root.resizable(0, 0)
root.title("tester")

app = Tester(root)

root.mainloop()