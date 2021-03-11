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
        self.canvas.itemconfigure(self.object_id, state="hiden")

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

class Contour(GameElement):
    def __init__(self, game_app, image_filename, x=0, y=0):
        self.image_filename = image_filename
        super().__init__(game_app, x, y)

    def render(self):
        self.photo_image = tk.PhotoImage(file=self.image_filename)
        self.canvas_object_id = self.canvas.create_image(
            self.x, 
            self.y,
            image=self.photo_image)