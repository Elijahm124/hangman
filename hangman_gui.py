import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk


class Hangman(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, GamePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='NSEW')
        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def show_level(self, difficulty):
        diff_label = tk.Label(self, text=f"{difficulty}", font=("Chalkboard", 20))
        diff_label.place(x=460, y=50)


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        image1 = Image.open("images/home_gallows.png")
        image1 = image1.resize((400, 598), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image1)

        label = tk.Label(self, image=test)
        label.image = test
        label.place(x=0, y=0)

        image2 = Image.open("images/stick.png")
        image2 = image2.resize((150, 150), Image.ANTIALIAS)
        test1 = ImageTk.PhotoImage(image2)
        label1 = tk.Label(self, image=test1)
        label1.image = test1
        label1.place(x=440, y=440)

        intro = tk.Label(self, text="Hangman!", font=("Chalkboard", 50))
        intro.place(x=330, y=50)

        intro2 = tk.Label(self, text="Select a difficulty", font=("Chalkboard", 25))
        intro2.place(x=335, y=150)

        easy_btn = tk.Button(self, text="Easy", font=("Chalkboard", 20),
                             command=lambda: [self.controller.show_frame("GamePage"), self.controller.show_level("Easy")])
        easy_btn.place(x=410, y=200)
        med_btn = tk.Button(self, text="Medium", font=("Chalkboard", 20),
                            command=lambda: [self.controller.show_frame("GamePage"), self.controller.show_level("Medium")])
        med_btn.place(x=400, y=250)
        hard_btn = tk.Button(self, text="Hard", font=("Chalkboard", 20),
                             command=lambda: [self.controller.show_frame("GamePage"), self.controller.show_level("Hard")])
        hard_btn.place(x=410, y=300)
        rand_btn = tk.Button(self, text="Random", font=("Chalkboard", 20),
                             command=lambda: [self.controller.show_frame("GamePage"), self.controller.show_level("Random")])
        rand_btn.place(x=400, y=350)


class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        intro = tk.Label(self, text="Hangman!", font=("Chalkboard", 35))
        intro.place(x=220, y=15)
        self.button = tk.Button(self, text="Go to the start page",
                                command=lambda: [controller.show_frame("HomePage"), self.reset_progress()])
        self.button.place(x=450, y=10)
        self.level = 0
        self.image1 = Image.open(f"images/gallows_{self.level}.png")
        self.image1 = self.image1.resize((185, 265))
        self.test = ImageTk.PhotoImage(self.image1)
        self.label1 = tk.Label(self, image=self.test)
        self.label1.image = self.test
        self.label1.place(x=25, y=85)
        self.button = tk.Button(self, text="change level",
                                command=lambda: self.change_level())
        self.button.place(x=500, y=500)

    def reset_progress(self):
        self.level = 0
        self.image1 = Image.open(f"images/gallows_{self.level}.png")
        self.image1 = self.image1.resize((185, 265))
        self.test = ImageTk.PhotoImage(self.image1)
        self.label1.config(image=self.test)
        self.label1.image = self.test

    def change_level(self):
        if self.level <= 7:
            self.level += 1
            self.image1 = Image.open(f"images/gallows_{self.level}.png")
            self.image1 = self.image1.resize((185, 265))
            self.test = ImageTk.PhotoImage(self.image1)
            self.label1.config(image=self.test)
            self.label1.image = self.test
        else:
            print("max tries exceeded")


if __name__ == "__main__":
    app = Hangman()
    app.title("Hangman")
    app.geometry("600x600")
    app.mainloop()

"""for i, v in enumerate("Hangman"):
    tk.Label(self, text=v, font=("Chalkboard", 40, "underline")).place(x=(265 + (i * 40)), y=50)"""
