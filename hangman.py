import random
from os import path
import tkinter as tk


def get_word_list():
    difficulty = ""
    while not path.exists(difficulty):
        difficulty = input("Type easy, medium, or hard: ")

        difficulty += "_words"

    with open(difficulty) as f:
        contents = f.readlines()

    word_list = [word.strip() for word in contents]

    return word_list


def get_word(word_list):
    word = random.choice(word_list)
    empty_word = ["_" for i in range(len(word))]
    return word, empty_word


def play(word, empty_word):
    used_letters = []
    correct_letters = []

    print(' '.join(empty_word))

    while len(used_letters) < 6 and len(correct_letters) < len(word):

        letter = input("Enter a letter: ")

        if not letter or len(letter) > 1:
            continue

        elif letter in word and letter not in correct_letters:
            for index, value in enumerate(word):
                if letter == value:
                    empty_word[index] = letter

            for i in range(word.count(letter)):
                if letter in word:
                    correct_letters.append(letter)

            print(f"correct {' '.join(empty_word)}")


        elif letter not in word and letter not in used_letters:
            used_letters.append(letter)
            print(f" wrong {used_letters}")

    print(word)


if __name__ == "__main__":
    word_list = get_word_list()
    word, empty_word = get_word(word_list)
    play(word, empty_word)
