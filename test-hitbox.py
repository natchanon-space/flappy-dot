import tkinter as tk
from gamelib import GameApp, Contour

class Tester(GameApp):
    def init_game(self):
        self.dot = Contour(self, "images/dot.png", x=100, y=250, show_hitbox=True)
        print("=== dot.png ===")
        print("img_width:", self.dot.photo_image.width(), "img_height:", self.dot.photo_image.height())
        print("hitbix", self.dot.hitbox.get_hitbox())

        self.upper_pillar = Contour(self, "images/pillar-top.png", x=200, y=100, show_hitbox=True)
        print("=== pillar-top.png ===")
        print("img_width:", self.upper_pillar.photo_image.width(), "img_height:", self.upper_pillar.photo_image.height())

        self.lower_pillar = Contour(self, "images/pillar-bottom.png", x=300, y=400, show_hitbox=True)
        print("=== pillar-top.png ===")
        print("img_width:", self.lower_pillar.photo_image.width(), "img_height:", self.lower_pillar.photo_image.height())

root = tk.Tk()
root.resizable(0, 0)
root.title("tester")

app = Tester(root)

root.mainloop()