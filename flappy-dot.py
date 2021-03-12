import tkinter as tk
import random
from gamelib import *

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

UPDATE_DELAY = 33
GRAVITY = 2 

PILLAR_SPEED = 5
STARTING_VELOCITY = -20
JUMP_VELOCITY = 30

class Dot(Contour):
    def init_element(self):
        self.vy = STARTING_VELOCITY
        self.is_started = False
    
    def update(self):
        if self.is_started:
            self.y += self.vy
            self.vy += GRAVITY
            #update hitbox
            self.hitbox_update()
    
    def start(self):
        self.is_started = True

    def jump(self):
        self.vy -= JUMP_VELOCITY

    def reset(self):
        self.is_started = False

    def get_coords(self):
        return (self.x, self.y)


class PillarPair():
    def __init__(self, game_app, space=150, show_hitbox=False, extend_x=0):
        self.is_started = False
        self.space = space
        self.extend_x = extend_x
        self.show_hitbox = show_hitbox

        # create pillars
        self.upper_pillar = Contour(game_app, "images/pillar-top.png", x=-500, y=0, show_hitbox=show_hitbox)
        self.lower_pillar = Contour(game_app, "images/pillar-bottom.png", x=-500, y=0, show_hitbox=show_hitbox)
        self.reset_pillars()

    def reset_pillars(self):
        # farthest place on x-axis
        self.upper_pillar.x = CANVAS_WIDTH + self.upper_pillar.width/2
        self.lower_pillar.x = CANVAS_WIDTH + self.lower_pillar.width/2
        # random space between pillars
        self.rand_point()
        self.upper_pillar.y = self.rp - self.space/2 - self.upper_pillar.height/2
        self.lower_pillar.y = self.rp + self.space/2 + self.lower_pillar.height/2

    # custom update
    def update(self):
        if self.is_started:
            self.upper_pillar.x -= PILLAR_SPEED
            self.lower_pillar.x -= PILLAR_SPEED
            if self.upper_pillar.x+self.upper_pillar.width/2 <= 0:
                self.reset_pillars()
            # update hitbox
            self.upper_pillar.hitbox_update()
            self.lower_pillar.hitbox_update()
        
    # custom render
    def render(self):
        self.upper_pillar.render()
        self.lower_pillar.render()

    def rand_point(self):
        self.rp = random.randint(self.space/2+10, CANVAS_HEIGHT-self.space/2-10)

    def start(self):
        self.is_started = True

    def reset(self):
        self.is_started = False

class FlappyDot(GameApp):
    def create_sprites(self):
        #create dot
        self.dot = Dot(self, 'images/dot.png', CANVAS_WIDTH//6, CANVAS_HEIGHT//2, show_hitbox=True)
        self.elements.append(self.dot)

        self.pillars = PillarPair(self, show_hitbox=True)
        self.elements.append(self.pillars)
        
    def init_game(self):
        self.canvas.config(background="lightgreen")
        self.create_sprites()
        self.score = 0
        self.text = Text(self, text=f"Score: {self.score}", x=50, y=20)
        self.elements.append(self.text)

    def on_key_pressed(self, event):
        if event.char == ' ':
            if not self.dot.is_started:
                self.dot.start()
                self.pillars.start()
            else:
                self.dot.jump()         

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Avocado Flight")
    root.resizable(0, 0)

    app = FlappyDot(root, CANVAS_WIDTH, CANVAS_HEIGHT)
    app.start()

    root.mainloop()