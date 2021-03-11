import tkinter as tk
import random
from gamelib import *

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

UPDATE_DELAY = 33
PILLAR_SPEED = 5

GRAVITY = 1

class PillarPair():
    def __init__(self, game_app, speed, expand_x=0, color="green"):
        self.canvas = game_app.canvas
        self.canvas_height = game_app.canvas_height
        self.canvas_width = game_app.canvas_width
        self.color = color
        self.speed = speed
        self.expand_x = expand_x

        self.create_pillars()
        
    def update(self):
        self.upper_pillar.x -= self.speed
        self.lower_pillar.x -= self.speed
        if self.upper_pillar.x + self.upper_pillar.size_x < 0:
            self.reset()

    def render(self):
        self.upper_pillar.render()
        self.lower_pillar.render()

    def create_pillars(self):
        self.set_pillars_info()
        self.upper_pillar = Contour(self, "r", color="blue", x=self.canvas_width+self.width+self.expand_x, y=self.upper_y, size_x=self.width, size_y=self.upper_height)
        self.lower_pillar = Contour(self, "r", color="red", x=self.canvas_width+self.width+self.expand_x, y=self.lower_y, size_x=self.width, size_y=self.lower_height)

    def set_pillars_info(self):
        rand_point = random.randint(100, self.canvas_height-100)
        space = 150
        self.width = self.canvas_width / 10

        self.upper_height = rand_point - space/2
        self.upper_y = self.upper_height/2

        self.lower_height = self.canvas_height - rand_point - space/2
        self.lower_y = self.canvas_height - self.lower_height/2

    def reset(self):
        self.set_pillars_info()
        self.upper_pillar.set_shape(self.canvas_width+self.width, self.upper_y, self.width, self.upper_height)
        self.lower_pillar.set_shape(self.canvas_width+self.width, self.lower_y, self.width, self.lower_height)

    def get_hitbox(self):
        return self.upper_pillar.get_hitbox(), self.lower_pillar.get_hitbox()

class FlappyDot(GameApp):
    def init_game(self):
        self.create_pillars()

        self.dot = Dot(self, "c", color="green", x=50, y=self.canvas_height/2, size_x=20, size_y=20)
        self.elements.append(self.dot)

        self.text = Text(self, text="Score: XX", x=50, y=20)
        self.elements.append(self.text)

    def create_pillars(self):
        for i in range(5):
            self.elements.append(PillarPair(self, PILLAR_SPEED, expand_x=i*190))

    def on_key_pressed(self, event):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(0, 0)

    app = FlappyDot(root, CANVAS_WIDTH, CANVAS_HEIGHT)
    app.start()

    # print(app.circle.get_hitbox())
    # print(app.rectangle.get_hitbox())
    # print(app.test_text.text)

    root.mainloop()