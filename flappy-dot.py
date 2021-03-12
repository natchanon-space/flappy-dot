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
        #create hitbox for dot
        self.hitbox = (-200, 0, -200, 0)
    
    def update(self):
        if self.is_started:
            self.y += self.vy
            self.vy += GRAVITY
            #update hitbox
            self.hitbox = (self.x-20, self.y-20, self.x+20, self.y+20)

    
    def start(self):
        self.is_started = True

    def jump(self):
        self.vy -= JUMP_VELOCITY

    def reset(self):
        self.is_started = False

    def get_coords(self):
        return (self.x, self.y)


class PillarPair(Contour):
    def init_element(self):
        self.x = 800
        self.y = 250
        self.is_started = False
        #create hitbox for each pillar
        self.hitbox_upper = (200, 0, 200, 0)
        self.hitbox_lower = (200, 0, 200, 0)
        

    def update(self):
        if self.is_started:
            #reset pillar location
            if self.x <= -50:
                self.x = 850
                #random hole(y) loaction
                self.y = random.choice([120, 200, 300, 380])
            else:
                self.x -= 10 
            #update hitbox
            self.hitbox_upper = (self.x-40, self.y-500, self.x+40, self.y-100)
            self.hitbox_lower = (self.x-40, self.y+98, self.x+40, self.y+500)
        

    def start(self):
        self.is_started = True

    def reset(self):
        self.is_started = False

    def get_coords(self):
        return (self.x, self.y)

class FlappyDot(GameApp):
    def create_sprites(self):
        #create dot
        self.dot = Dot(self, 'images/dot.png', CANVAS_WIDTH // 6, CANVAS_HEIGHT // 2)
        self.elements.append(self.dot)
        
        #creat a pair of pillar
        self.pillar_pair = PillarPair(self, 'images/pillar-pair.png', CANVAS_WIDTH, CANVAS_HEIGHT // 2)
        self.elements.append(self.pillar_pair)

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
                self.pillar_pair.start()
            else:
                self.dot.jump()
        #update score
        self.score_display()
        #hitbox check
        self.hit_check()
    

    def score_display(self):
        if self.dot.hitbox[0] == self.pillar_pair.hitbox_upper[2]:
            self.score += 1
            self.text = Text(self, text=f"Score: {self.score}", x=50, y=20)
            self.elements.append(self.text)

    
    def hit_check(self):
        if self.dot.hitbox[1] < self.pillar_pair.hitbox_upper[3] or self.dot.hitbox[3] > self.pillar_pair.hitbox_lower[1]:
            if (self.dot.hitbox[2] > self.pillar_pair.hitbox_upper[0] and self.dot.hitbox[2] < self.pillar_pair.hitbox_upper[2]) or \
                (self.dot.hitbox[0] > self.pillar_pair.hitbox_upper[0] and self.dot.hitbox[0] < self.pillar_pair.hitbox_upper[2]):
                #Game Over
                exit() 
               

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Avocado Flight")
    root.resizable(0, 0)

    app = FlappyDot(root, CANVAS_WIDTH, CANVAS_HEIGHT)
    app.start()

    root.mainloop()