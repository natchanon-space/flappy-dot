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

class Dot(Sprite):
    def init_element(self):
        self.vy = STARTING_VELOCITY
        self.is_started = False

    def update(self):
        if self.is_started:
            self.y += self.vy
            self.vy += GRAVITY
            # update hit box
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
    def __init__(self, game_app, space=200, show_hitbox=False, extend_x=0):
        self.is_started = False
        self.space = space
        self.extend_x = extend_x
        self.show_hitbox = show_hitbox

        # passing check
        self.is_passed = False

        # create pillars
        # change create lower pillar location
        self.upper_pillar = Sprite(game_app, "images/pillar-top.png", x=500, y=0, show_hitbox=show_hitbox)
        self.lower_pillar = Sprite(game_app, "images/pillar-bottom.png", x=500, y=0, show_hitbox=show_hitbox)
        self.reset_pillars(is_init=True)

    def reset_pillars(self, is_init=False):
        # farthest place on x-axis
        if is_init:
            self.upper_pillar.x = CANVAS_WIDTH + self.upper_pillar.width / 2 + self.extend_x
            self.lower_pillar.x = CANVAS_WIDTH + self.lower_pillar.width / 2 + self.extend_x
        else:
            self.upper_pillar.x = CANVAS_WIDTH + self.upper_pillar.width / 2
            self.lower_pillar.x = CANVAS_WIDTH + self.lower_pillar.width / 2

        # random space between pillars
        self.rand_point()
        self.upper_pillar.y = self.rp - self.space / 2 - self.upper_pillar.height / 2
        self.lower_pillar.y = self.rp + self.space / 2 + self.lower_pillar.height / 2

    # custom update
    def update(self):
        if self.is_started:
            self.upper_pillar.x -= PILLAR_SPEED
            self.lower_pillar.x -= PILLAR_SPEED
            # reset passed status and coords
            if self.upper_pillar.x + self.upper_pillar.width / 2 <= 0:
                self.reset_pillars()
                self.is_passed = False
            # update hit box
            self.upper_pillar.hitbox_update()
            self.lower_pillar.hitbox_update()

    # custom render
    def render(self):
        self.upper_pillar.render()
        self.lower_pillar.render()

    def rand_point(self):
        self.rp = random.randint(self.space / 2 + 10, CANVAS_HEIGHT - self.space / 2 - 10)

    def start(self):
        self.is_started = True

    def reset(self):
        self.is_started = False

class FlappyDot(GameApp):
    def create_sprites(self):
        # create dot
        self.dot = Dot(self, 'images/dot.png', CANVAS_WIDTH // 6, CANVAS_HEIGHT // 2, show_hitbox=False)

        # separate dot and pillar from elements (it's easier for collision checking :D)
        self.pillars = []
        for i in range(4):
            self.pillars.append(PillarPair(self, show_hitbox=False, extend_x=i*220))

        self.elements = [p for p in self.pillars]
        self.elements.append(self.dot) 

    def init_game(self, restart=False):
        # restart setup
        self.elements = []
        self.score = 0

        self.canvas.config(background="lightgreen")
        self.create_sprites()

        if not restart:
            self.text = Text(self, text=f"Score: {self.score:.0f}", x=50, y=20, font=('Garamond', 20))
            self.start_txt = Text(self, text=f"Press Spacebar to Start", x=CANVAS_WIDTH/2, y=CANVAS_HEIGHT/2+70, font=('Garamond', 50))

        self.canvas.tag_raise(self.text.object_id)
        self.canvas.tag_raise(self.start_txt.object_id)

    def on_key_pressed(self, event):
        if event.char == ' ':
            if not self.dot.is_started:
                self.start_txt.hide()
                self.dot.start()
                for p in self.pillars:
                    p.start()
            else:
                self.dot.jump()
        
        if event.char == "s" and self.collision():
            self.text.set_text(text=f"Score: {self.score:.0f}")
            self.start_txt.hide()
            self.init_game(restart=True)
            self.start()

        if event.char == "q":
            self.parent.destroy()

    # new version of collision
    def collision(self):
        dot_hitbox = self.dot.hitbox.get_hitbox()  # x1, y1, x2, y2

        # upper floor collide
        if dot_hitbox[1] < -300:
            return True

        # lower floor collide
        if dot_hitbox[3] > CANVAS_HEIGHT + 10:
            return True
        # all pillars collide
        for pillars in self.pillars:
            upper_hitbox = pillars.upper_pillar.hitbox.get_hitbox()
            lower_hitbox = pillars.lower_pillar.hitbox.get_hitbox()
            # upper pillar
            if upper_hitbox[0] <= dot_hitbox[2] <= upper_hitbox[2] and upper_hitbox[1] <= dot_hitbox[1] <= upper_hitbox[
                3]:
                return True
            # lower pillar
            if lower_hitbox[0] <= dot_hitbox[2] <= lower_hitbox[2] and lower_hitbox[1] <= dot_hitbox[3] <= lower_hitbox[
                3]:
                return True
        # base case
        return False

    def check_score(self):
        dot_hitbox = self.dot.hitbox.get_hitbox()
        for pillars in self.pillars:
            upper_hitbox = pillars.upper_pillar.hitbox.get_hitbox()
            lower_hitbox = pillars.lower_pillar.hitbox.get_hitbox()
            if dot_hitbox[2] >= upper_hitbox[2] and not pillars.is_passed:
                self.score += 1
                pillars.is_passed = True
        self.text.set_text(f"Score: {self.score:.0f}")

    def animate(self):
        for elem in self.elements:
            elem.update()
            elem.render()
        self.check_score()

        if self.collision():
            self.start_txt.set_text(text=f"{'You lose!':^22}\n{f'Score: {self.score:.0f}':^22}\n(Press 'S' to Restart)")
            self.start_txt.show()
            return

        self.after_id = self.after(self.update_delay, self.animate)

def main():
    root = tk.Tk()
    root.title("Avocado Flight")
    root.resizable(0, 0)

    app = FlappyDot(root, CANVAS_WIDTH, CANVAS_HEIGHT)
    app.start()

    root.mainloop()

if __name__ == "__main__":
    main()

