import tkinter
import tkinter as tk
from PIL import Image, ImageTk

window = tk.Tk()
window.title("Hangman")
window.geometry("600x600")

def home_page():
    image1 = Image.open("gallows.png")
    image1 = image1.resize((550, 635), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(image1)

    label = tkinter.Label(image=test)
    label.image = test

    label.place(x=-175, y=0)

    intro = tk.Label(text="Hangman!", font=("Chalkboard", 50))
    intro.place(x=200, y=100)

    intro2 = tk.Label(text="Select a difficulty", font=("Chalkboard", 25))
    intro2.place(x=200, y=250)

    easy_btn = tk.Button(text="Easy", font=("Chalkboard", 20))
    easy_btn.place(x=280, y=300)
    med_btn = tk.Button(text="Medium", font=("Chalkboard", 20))
    med_btn.place(x=268, y=350)
    hard_btn = tk.Button(text="Hard", font=("Chalkboard", 20))
    hard_btn.place(x=280, y=400)
    rand_btn = tk.Button(text="Random", font=("Chalkboard", 20))
    rand_btn.place(x=268, y=450)

while True:

    window.mainloop()
