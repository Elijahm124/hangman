import random
from os import path


def get_word_list():
    difficulty = ""
    while not path.exists(f"word_lists/{difficulty}_words"):
        difficulty = input("Type easy, medium, or hard: ")


    with open(f"word_lists/{difficulty}_words") as f:
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
