import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import random


class Hangman(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        self.container = container
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.diff_label = None
        self.word_list = []
        self.word = ""
        self.empty_letters = []
        self.difficulty = None

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

    def delete_level(self):
        self.diff_label.place_forget()
        for i in self.empty_letters.copy():
            i.place_forget()
        self.empty_letters.clear()

    def show_level(self, difficulty):
        self.diff_label = tk.Label(self, text=f"{difficulty.title()}", font=("Chalkboard", 20))
        self.diff_label.place(x=460, y=50)
        self.difficulty = difficulty

    def generate_word_list(self, difficulty):
        if self.word_list:
            self.word_list = []
        if difficulty in ["easy", "medium", "hard"]:
            with open(f"word_lists/{difficulty}_words") as f:
                contents = f.readlines()

            self.word_list = [word.strip().lower() for word in contents]
        else:
            with open("word_lists/easy_words") as e, open("word_lists/medium_words") as m, open(
                    "word_lists/hard_words") as h:

                easy = e.readlines()
                med = m.readlines()
                hard = h.readlines()
                contents = easy + med + hard

            self.word_list = [word.strip().lower() for word in contents]

        return self.word_list

    def get_word(self, difficulty):
        if self.word:
            self.word = ""
        word = random.choice(self.generate_word_list(difficulty))
        self.word = word

    def show_empty_word(self):
        for i in range(len(self.word)):
            letter = tk.Label(self, text="_", font=("Chalkboard", 40))
            letter.place(x=100 + (i * 37), y=400, anchor="center")
            self.empty_letters.append(letter)


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
                             command=lambda: [self.controller.show_frame("GamePage"),
                                              self.controller.show_level("easy"),
                                              self.controller.get_word("easy"),
                                              self.controller.show_empty_word()])
        easy_btn.place(x=410, y=200)
        med_btn = tk.Button(self, text="Medium", font=("Chalkboard", 20),
                            command=lambda: [self.controller.show_frame("GamePage"),
                                             self.controller.show_level("medium"),
                                             self.controller.get_word("medium"),
                                             self.controller.show_empty_word()])
        med_btn.place(x=400, y=250)
        hard_btn = tk.Button(self, text="Hard", font=("Chalkboard", 20),
                             command=lambda: [self.controller.show_frame("GamePage"),
                                              self.controller.show_level("hard"),
                                              self.controller.get_word("hard"),
                                              self.controller.show_empty_word()])
        hard_btn.place(x=410, y=300)
        rand_btn = tk.Button(self, text="Random", font=("Chalkboard", 20),
                             command=lambda: [self.controller.show_frame("GamePage"),
                                              self.controller.show_level("random"),
                                              self.controller.get_word("random"),
                                              self.controller.show_empty_word()])
        rand_btn.place(x=400, y=350)


class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        intro = tk.Label(self, text="Hangman!", font=("Chalkboard", 35))
        intro.place(x=220, y=15)
        self.button = tk.Button(self, text="Main Menu",
                                command=lambda: [self.controller.delete_level(), self.controller.show_frame("HomePage"),
                                                 self.reset_progress()])
        self.button.place(x=75, y=30)
        self.level = 0
        self.image1 = Image.open(f"images/gallows_{self.level}.png")
        self.image1 = self.image1.resize((185, 265))
        self.test = ImageTk.PhotoImage(self.image1)
        self.label1 = tk.Label(self, image=self.test)
        self.label1.image = self.test
        self.label1.place(x=25, y=85)
        self.letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.letter_dic = {}
        self.clicked_letters = []
        self.image2 = Image.open("images/used_words_box.png")
        self.image2 = self.image2.resize((130, 155))
        self.test1 = ImageTk.PhotoImage(self.image2)
        self.label2 = tk.Label(self, image=self.test1)
        self.label2.image = self.test1
        self.label2.place(x=440, y=140)
        self.used_words_str = tk.Label(self, text="Used Words", font=("Chalkboard", 19))
        self.used_words_str.place(x=455, y=110)
        self.missed_letter_objects = []
        self.missed_count, self.correct_count = 0, 0
        self.used_coordinates = {}
        self.end_string, self.correct_word = None, None
        self.game_ended = False
        self.restart_button = tk.Button(self, text="Restart",
                                        command=lambda: [self.reset_progress(), self.restart_game()])
        self.restart_button.place(x=20, y=30)
        for i in range(4):
            self.used_coordinates[i] = (450 + (i * 25), 150)
        for i in range(4, 8):
            self.used_coordinates[i] = (450 + (i - 4) * 25, 185)
        for i in range(8, 12):
            self.used_coordinates[i] = (450 + (i - 8) * 25, 220)
        for i in range(12, 16):
            self.used_coordinates[i] = (450 + (i - 12) * 25, 255)

        for letter in self.letters[:13]:
            index = self.letters.index(letter)
            letter_button = tk.Button(self, text=letter, command=lambda letter=letter: self.select_letter(letter))
            letter_button.place(x=50 + (index * 35), y=495, anchor="center")
            self.letter_dic[index] = letter_button
        for letter in self.letters[13:]:
            index = self.letters.index(letter)
            letter_button = tk.Button(self, text=letter, command=lambda letter=letter: self.select_letter(letter))
            letter_button.place(x=50 + ((index - 13) * 35), y=545, anchor="center")
            self.letter_dic[index] = letter_button

    def check_end_game(self):

        if self.level > 6:
            self.end_string = tk.Label(self, text="You Lose!", font=("Chalkboard", 24))
            self.end_string.place(x=260, y=280)
            self.correct_word = tk.Label(self, text=f"Correct Word: {self.controller.word.title()}",
                                         font=("Chalkboard", 20))
            self.correct_word.place(x=260, y=330)

            for button in self.letter_dic.values():
                button["state"] = "disable"
        elif self.correct_count == len(self.controller.word):
            self.end_string = tk.Label(self, text="You Win!", font=("Chalkboard", 24))
            self.end_string.place(x=260, y=280)
            for button in self.letter_dic.values():
                button["state"] = "disable"

    def select_letter(self, letter):
        if self.level <= 6:
            if letter.lower() not in self.controller.word:
                try:
                    missed_letter = tk.Label(self, text=letter, font=("Chalkboard", 22))
                    missed_letter.place(x=self.used_coordinates[self.missed_count][0],
                                        y=self.used_coordinates[self.missed_count][1])
                except KeyError:
                    print("max tries exceeded")
                else:
                    self.change_level()
                    self.missed_letter_objects.append(missed_letter)
                    self.missed_count += 1
            else:
                for index, value in enumerate(self.controller.word):
                    if value == letter.lower():
                        self.correct_count += 1
                        self.controller.empty_letters[index].config(text=letter)

            self.clicked_letters.append(letter)
            index = self.letters.index(letter)
            button = self.letter_dic[index]
            button.place_forget()
        self.check_end_game()

    def reset_progress(self):
        self.level = 0
        self.missed_count, self.correct_count = 0, 0
        self.image1 = Image.open(f"images/gallows_{self.level}.png")
        self.image1 = self.image1.resize((185, 265))
        self.test = ImageTk.PhotoImage(self.image1)
        self.label1.config(image=self.test)
        self.label1.image = self.test
        if self.clicked_letters:
            for letter in self.clicked_letters:
                index = self.letters.index(letter)
                if letter in self.letters[:13]:
                    letter_button = tk.Button(self, text=letter,
                                              command=lambda letter=letter: self.select_letter(letter))
                    letter_button.place(x=50 + (index * 35), y=495, anchor="center")
                    self.letter_dic[index] = letter_button
                elif letter in self.letters[13:]:
                    letter_button = tk.Button(self, text=letter,
                                              command=lambda letter=letter: self.select_letter(letter))
                    letter_button.place(x=50 + ((index - 13) * 35), y=545, anchor="center")
                    self.letter_dic[index] = letter_button
            self.clicked_letters.clear()
        if self.missed_letter_objects:
            for i in self.missed_letter_objects:
                i.destroy()
            self.missed_letter_objects.clear()
        if self.end_string:
            self.end_string.destroy()
            self.end_string = None
        if self.correct_word:
            self.correct_word.destroy()
            self.correct_word = None
        for button in self.letter_dic.values():
            button["state"] = "normal"

    def restart_game(self):
        for letter in self.controller.empty_letters:
            letter.destroy()
        self.controller.empty_letters = []
        self.controller.get_word(self.controller.difficulty)
        self.controller.show_empty_word()

    def change_level(self):
        if self.level <= 6:
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


    #If click buttons after game ends, text stays on

"""for i, v in enumerate("Hangman"):
    tk.Label(self, text=v, font=("Chalkboard", 40, "underline")).place(x=(265 + (i * 40)), y=50)"""
