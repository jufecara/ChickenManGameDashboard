from tkinter import Tk, Button, Canvas, Label
from commands import reset_all


class App(Tk):
    rel_entrywidth_y = 0.02
    HEIGHT = 480
    WIDTH = 640

    def call_reset_all(self):
        reset_all()

    def __init__(self):
        super().__init__()
        self.title("Dashboard")
        self.create_widgets()


    def create_widgets(self):
        self.canvas = Canvas(self, width=self.WIDTH, height=self.HEIGHT, bg='#adadad')
        self.canvas.pack()

        self.winner_label = Label(self.canvas, text="Winner")
        self.winner_label.place(anchor='nw', relx=0.01, rely=self.rel_entrywidth_y, relwidth=0.18, relheight=0.05)


        # btn = Button(self.window, text="Reset Game", command=self.call_reset_all)
        # btn.grid(column=1, row=0)

        # self.window.geometry("640x480")
        # self.window.attributes('-fullscreen', True)
        # self.window.overrideredirect(True)

        # self.window.mainloop()


