"""
CSSE1001 Assignment 1
Semester 2, 2020
"""

import random

__author__ = "Mike Smith"
__email__ = "dongming.shi@uqconnect.edu.au"
__date__ = "04/09/20"


WORDS_PATH = "./words"

GUESS_INDEX_TUPLE = (
    ((0, 1), (2, 4), (2, 4), (3, 5), (2, 5), (0, 5)),  # len: 6
    ((0, 1), (1, 2), (4, 6), (2, 5), (3, 6), (2, 6), (0, 6)),  # len: 7
    ((0, 1), (1, 3), (4, 7), (3, 5), (3, 6), (5, 7), (2, 7), (0, 7)),  # len: 8
    ((0, 1), (1, 3), (4, 7), (3, 5), (3, 6), (5, 7), (3, 7), (2, 8), (0, 8)),  # len: 9
)

WALL_VERTICAL = "|"
WALL_HORIZONTAL = "-"
SPACE = " "

VOWELS = "aeiou"
CONSONANTS = "bcdfghjklmnpqrstvwxyz"

WELCOME = """
Welcome to the Criss-Cross Multi-Step Word Guessing Game!
"""

INPUT_ACTION = """
Enter an input action. Choices are:
s - start game
h - get help on game rules
q - quit game: 
"""

HELP = """
Game rules - You have to guess letters in place of the asterixis. 
Each vowel guessed in the correct position gets 14 points. 
Each consonant guessed in the correct position gets 12 points. 
Each letter guessed correctly but in the wrong position gets 5 points. 
If the true letters were "dog", say, and you guessed "hod", 
you would score 14 points for guessing the vowel, "o", in the correct 
position and 5 points for guessing "d" correctly, but in the 
incorrect position. Your score would therefore be 19 points.
"""

INVALID = """
Please enter a valid command.
"""


def load_words(word_select):
    """
    Loading in the selection of words from either the FIXED or ARBITRARY word
    length.

    Parameters:
        word_select (str): "FIXED" or "ARBITRARY" word sets.
    Returns:
        (tuple<str>): A tuple containing all the words.
    """
    words = ()

    with open(f"{WORDS_PATH}/WORDS_{word_select}.txt", "r") as file:
        file_contents = file.readlines()

    for line in file_contents:
        word = line.strip()
        if word != "":
            words += (word,)

    return words


def random_index(words):
    """
    (int): Returns an int representing the index for the word to be guessed.
    """
    return random.randrange(0, len(words))


def game_mode():
    """
    Prompt the user to select the game mode

    """
    input_letter = input(INPUT_ACTION)

    if input_letter == "s":
        return start_game()

    elif input_letter == "h":
        print(HELP)
        return start_game()

    elif input_letter == "q":
        return "q"

    else:
        print(INVALID)
        return game_mode()


def start_game():
    """
    Prompts the user to select the game difficulty

    """
    game_level = input("Do you want a 'FIXED' or 'ARBITRARY' length word?: ")

    if game_level == "FIXED" or game_level == "ARBITRARY":
        return game_level

    else:
        word_inp = start_game()
        return word_inp


def select_word_at_random(word_select):
    """
    Randomly selects word base on difficulty selected by the user

    """
    if word_select == "FIXED" or word_select == "ARBITRARY":
        words = load_words(word_select)
        ind = int(random_index(words))
        word = words[ind]
        return word

    else:
        return


def create_guess_line(guess_no, word_length):
    """
    Returns the current guess line

    """
    GIT_word = GUESS_INDEX_TUPLE[word_length - 6]
    GIT_start, GIT_end = GIT_word[guess_no - 1]
    display = ""
    count = 0

    """ Prints '*' in the guess index position, prints '-' otherwise """
    while count < word_length:
        if count >= GIT_start and count <= GIT_end:
            display += f"{WALL_VERTICAL} * "
        else:
            display += f"{WALL_VERTICAL} - "

        count += 1

    return f"Guess {guess_no}{display}{WALL_VERTICAL}"


def display_guess_matrix(guess_no, word_length, scores):
    """
    Prints the progress of the game

    """
    letter = 0
    count_1 = 0
    count_2 = 0
    display = ""
    dash = 9 * WALL_HORIZONTAL
    output = ""

    while count_1 < word_length:
        letter += 1
        display += f"{WALL_VERTICAL} {letter} "
        dash += 4 * WALL_HORIZONTAL
        count_1 += 1

    while count_2 < guess_no - 1:
        past_lines = f"{create_guess_line(count_2 + 1, word_length)}{3 * SPACE}{scores[count_2]} Points"
        output += f"\n{dash}\n{past_lines}"
        count_2 += 1

    current_line = create_guess_line(guess_no, word_length)
    print(f"{7 * SPACE}{display}{WALL_VERTICAL}{output}")
    print(f"{dash}\n{current_line}")
    print(dash)


def compute_value_for_guess(word, start_index, end_index, guess):
    """
    Calculates the scores for the game

    """
    substring = word[start_index : end_index + 1]
    score = 0
    index = 0

    for letter in range(start_index, end_index + 1):
        if guess[index] == substring[index]:
            if guess[index] in VOWELS:
                score += 14
            else:
                score += 12

        elif guess[index] in substring:
            score += 5

        else:
            score += 0

        index += 1

    return score


def main():
    """
    Handles top-level interaction with user.
    """
    print(WELCOME)

    word_select = game_mode()
    if word_select == "q":
        return

    word = select_word_at_random(word_select)
    word_length = len(word)

    print("Now try and guess the word, step by step!!")

    guess_no = 0
    count = 0
    display = ""
    scores = ()

    while count < word_length:
        guess_no += 1
        count += 1

        GIT_word = GUESS_INDEX_TUPLE[word_length - 6]
        GIT_letter = GIT_word[guess_no - 1]
        start_index = GIT_letter[0]
        end_index = GIT_letter[1]

        display_guess_matrix(guess_no, word_length, scores)

        if guess_no == word_length:
            guess = input("Now enter your final guess. i.e. guess the whole word: ")

        else:
            guess = input(f"Now enter Guess {guess_no}: ")

            while len(guess) != len(word[start_index : end_index + 1]):
                guess = input(f"Now enter Guess {guess_no}: ")

        scores += (compute_value_for_guess(word, start_index, end_index, guess),)

    if guess == word:
        print("You have guessed the word correctly. Congratulations.")

    else:
        print(f'Your guess was wrong. The correct word was "{word}"')


if __name__ == "__main__":
    main()
