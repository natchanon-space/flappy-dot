import tkinter as tk
import tkinter.ttk as ttk


class GameApp(ttk.Frame):
    def __init__(self, parent, canvas_width=800, canvas_height=500, update_delay=33):
        super().__init__(parent)
        
        # initial constant
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.update_delay = update_delay
        self.parent = parent
        self.grid(sticky="nsew")
        # create and setup canvas
        self.create_canvas()
        # game_elements setting
        self.elements = []
        self.init_game()
        # keyboard-event binding
        self.parent.bind("<KeyPress>", self.on_key_pressed)
        self.parent.bind("<KeyRelease>", self.on_key_released)

    def create_canvas(self):
        self.canvas = tk.Canvas(self, borderwidth=0, width=self.canvas_width, height=self.canvas_height)
        self.canvas.grid(sticky="nsew")
        
    def animate(self):
        for elem in self.elements:
            elem.update()
            elem.render()
        self.after_id = self.after(self.update_delay, self.animate)

    def start(self):
        self.after_id = self.after(0, self.animate)

    def init_game(self):
        # game init setup for sub-class
        pass

    def on_key_pressed(self, event):
        pass

    def on_key_released(self, event):
        pass
    

class GameElement():
    def __init__(self, game_app, x=0, y=0):
        self.x = x
        self.y = y
        self.canvas = game_app.canvas

        self.is_visible = True

        self.init_canvas_object()
        self.init_element()

    def show(self):
        self.is_visible = True
        self.canvas.itemconfigure(self.object_id, state="normal")

    def hide(self):
        self.is_visible = False
        self.canvas.itemconfigure(self.object_id, state="hidden")

    def update(self):
        pass

    def render(self):
        if self.is_visible:
            self.canvas.coords(self.object_id, self.x, self.y)

    def init_canvas_object(self):
        """ init canvas object """
        pass

    def init_element(self):
        """ init element properties """
        pass


class Text(GameElement):
    def __init__(self, game_app, text, x=0, y=0):
        self.text = text
        super().__init__(game_app, x, y)
        
    def init_canvas_object(self):
        self.object_id = self.canvas.create_text(self.x, self.y, text=self.text)

    def set_text(self, text):
        self.text = text
        self.canvas.itemconfigure(self.object_id, text=self.text)


class Sprite(GameElement):
    def __init__(self, game_app, image_filename, x=0, y=0, show_hitbox=False):
        self.image_filename = image_filename
        self.show_hitbox = show_hitbox
        super().__init__(game_app, x, y)
        # show/hide hitbox
        self.hitbox = Hitbox(game_app, x, y, self.width, self.height)
        if self.show_hitbox:
            self.hitbox.show()
        else:
            self.hitbox.hide()

    # replace previous render for smoother motions
    def init_canvas_object(self):
        self.photo_image = tk.PhotoImage(file=self.image_filename)
        self.width = self.photo_image.width()
        self.height = self.photo_image.height()
        self.object_id = self.canvas.create_image(
            self.x, 
            self.y,
            image=self.photo_image)

    def hitbox_update(self):
        self.hitbox.x = self.x
        self.hitbox.y = self.y

    def render(self):
        super().render()
        self.hitbox.render()


class Hitbox(GameElement):
    def __init__(self, game_app, x, y, width, height):
        self.width = width
        self.height = height
        super().__init__(game_app, x, y)

    def init_canvas_object(self):
        self.object_id = self.canvas.create_rectangle(self.x-self.width/2, self.y-self.height/2, self.x+self.width/2, self.y+self.height/2)

    def get_hitbox(self):
        return self.x-self.width/2, self.y-self.height/2, self.x+self.width/2, self.y+self.height/2

    def render(self):
        if self.is_visible:
            self.canvas.coords(self.object_id, self.x-self.width/2, self.y-self.height/2, self.x+self.width/2, self.y+self.height/2)