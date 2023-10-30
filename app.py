from tkinter import Tk, Button
from commands import reset_all



class App():

    window = None

    def call_reset_all(self):
        reset_all()

    def __init__(self):
        self.window = Tk()
        self.window.title("Welcome")
        btn = Button(self.window, text="Reset Game", command=self.call_reset_all)
        btn.grid(column=1, row=0)

        self.window.mainloop()


