import csv
import hashlib
import random
import re
import sys


words_file = "database/word.csv"
Words_meaning = "database/wm.csv"
country_names_file = "database/country_name.csv"
spelling_file = "database/spelling_file.csv"
users_file = "database/users.csv"
score_file = "database/scores.csv"




def terminator(t):
    if t == 3:
        print("Limit Reach out try again ")
        sys.exit()


def add_score(username, score):
    # Read existing scores
    existing_scores = {}
    with open(score_file, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            existing_scores[row[0]] = row[1]
    # Update existing score if username exists, otherwise add new score
    existing_scores[username] = str(score)

    # Write scores to CSV file
    with open(score_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for user, score in existing_scores.items():
            writer.writerow([user, score])


# User authentication functions
def register(username, password, userfile):
    with open(userfile, "r", newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username:
                # checking if username already exist or not
                print("Username already exists. Please Register with another username.")
                return True

    # If username doesn't exist then register the user
    with open(userfile, "a", newline='') as file:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        writer = csv.writer(file)
        writer.writerow([username, hashed_password])
    return False


def login(username, password, userfile):
    with open(userfile, "r", newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            stored_username, stored_password = row
            if stored_username == username:
                if hashlib.sha256(password.encode()).hexdigest() == stored_password:
                    return False
    return True

# validate password
def password_validator(password):
    # Define a regular expression for special characters and digits
    special_characters = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')
    numbers = re.compile(r'[0-9]')

    # Check if the length is at least 8 characters
    if len(password) > 8:

        if special_characters.search(password) and numbers.search(password):
            return password
    return False

# getting a word from csv file
def load_word():
    with open(words_file, "r") as file:
        # same as above
        reader = csv.reader(file)
        # converting readerobect into list
        reader = list(reader)
        # print(reader)
        word = random.choice(reader)
        # word 1 list hai jis k 0 index pr string pri hai us ko pick krny k liay word[0] lgaya hai
        return word[0]

# getting a sentence and its meaning from csv file
def load_definition():
    with open(Words_meaning, "r", encoding="utf8") as file:
        reader = csv.reader(file)
        reader = list(reader)
        data = random.choice(reader)
        a, b = data[0], data[1]
        return a, b

def load_spellings():
    with open(spelling_file, "r") as file:
        reader = csv.reader(file)
        reader = list(reader)
        data = random.choice(reader)
        # print(data)
        a, b = data[0], data[1]
        return a, b

################# Game Functions ################
# function for words definition game The 2nd game
def words_definition_game():
    score = 0
    wrong_guess = 0
    difficulty = [10, 6, 3]
    mastered_definition = []
    while True:
        chose_difficulty = int(input(
            f"{">" * 20} Enter Your difficulty level {"<" * 20} \n0: Easy (10 lives)\n1: Medium (6 lives)\n2: Hard (3 lives)\n"))
        if chose_difficulty == 0 or chose_difficulty == 1 or chose_difficulty == 2:
            break
        else:
            print("Invalid choice please try again")

    life = difficulty[chose_difficulty]

    while life != wrong_guess:
        word, sentence = load_definition()
        # for testing
        print(word)
        guess = input(f'Enter the Definition of Sentence "{sentence}"\n')

        if guess == word.lower():
            score += 1
            definition = [word, sentence]
            mastered_definition.append(definition)
        else:
            print("Wrong Guess")
            wrong_guess += 1

        print(f"{">" * 20} Mastered definition  | {mastered_definition} {"<" * 20}")
        print(f"{">" * 20} Score {score} {"<" * 20}")
        print(f"{">" * 20} Remaining life {life - wrong_guess} {"<" * 20}")
        print(f"{">" * 20} Wrong guesses {wrong_guess} {"<" * 20}")
    print("End Lives")
    # adding score to scores.csv file
    add_score(username, score)


# function for word guessing game
def word_guessing_game():
    score = 0
    wrong_guess = 0
    difficulty = [10, 6, 3]
    mastered_words = []
    while True:
        chose_difficulty = int(input(f"{">" * 20} Enter Your difficulty level {"<" * 20} \n0: Easy (10 lives)\n1: Medium (6 lives)\n2: Hard (3 lives)\n"))
        if chose_difficulty == 0 or chose_difficulty == 1 or chose_difficulty == 2:
            break
        else:
            print("Invalid choice please try again")
    life = difficulty[chose_difficulty]
    while life != wrong_guess:
        word = load_word()
        # for testing
        print(word)
        guess = input(f'Guess the word which has "{len(word)}" letters,  starts with "{word[0]}" middle is "{word[int(len(word) / 2)]}" and end with "{word[-1]}" \n')

        if guess == word:
            score += 1
            mastered_words.append(word)
        else:
            print("Wrong Guess ")
            wrong_guess += 1
        print(f"{">" * 20} Mastered Words  | {mastered_words} {"<" * 20}")
        print(f"{">" * 20} Score {score} {"<" * 20}")
        print(f"{">" * 20} Remaining life {life - wrong_guess} {"<" * 20}")
        print(f"{">" * 20} Wrong guesses {wrong_guess} {"<" * 20}")
    print("End lives ")
    add_score(username, score)


def spell_corrector():
    score = 0
    wrong_guess = 0
    difficulty = [10, 6, 3]
    correct_spelling = []
    while True:
        chose_difficulty = int(input(
            f"{">" * 20} Enter Your difficulty level {"<" * 20} \n0: Easy (10 lives)\n1: Medium (6 lives)\n2: Hard (3 lives)\n"))
        if chose_difficulty == 0 or chose_difficulty == 1 or chose_difficulty == 2:
            break
        else:
            print("Wrong Spelling please try again")

    life = difficulty[chose_difficulty]
    while life != wrong_guess:
        right_word, wrong_word = load_spellings()
        # for testing
        print(right_word)
        spell_input = input(f'Enter the correct spelling of word "{wrong_word}"\n')
        if spell_input == right_word.lower():
            score += 1
            correct_spelling.append(right_word)
        else:
            print("Wrong Spelling")
            wrong_guess += 1

        print(f"{">" * 20} Correct spellings  | {correct_spelling} {"<" * 20}")
        print(f"{">" * 20} Score {score} {"<" * 20}")
        print(f"{">" * 20} Remaining life {life - wrong_guess} {"<" * 20}")
        print(f"{">" * 20} Wrong guesses {wrong_guess} {"<" * 20}")
    print("End Lives")
    # adding score to scores.csv file
    add_score(username, score)


def country_chain_game():
    score = 0
    wrong_guess = 0
    difficulty = [10, 6, 3]
    guessed_country = []
    country_list = []
    while True:
        chose_difficulty = int(input(
            f"{">" * 20} Enter Your difficulty level {"<" * 20} \n0: Easy (10 lives)\n1: Medium (6 lives)\n2: Hard (3 lives)\n"))
        if chose_difficulty == 0 or chose_difficulty == 1 or chose_difficulty == 2:
            break
        else:
            print("Invalid choice please try again")

    life = difficulty[chose_difficulty]
    with open(country_names_file, "r") as file:
        for row in file:
            country_list.append(row.strip())

    while life != wrong_guess:
        start_country = random.choice(country_list)
        new_country = input(f"Enter the country start with the ending letter of '{start_country}'\n").title()

        if new_country in country_list and new_country not in guessed_country and new_country[0].lower() == start_country[-1].lower():
            guessed_country.append(new_country)
            score += 1
        elif new_country in country_list and new_country in guessed_country and new_country[0].lower() == start_country[-1].lower():
            print("Already guessed that country")
        else:
            print("Wrong Guess")
            wrong_guess += 1

        print(f"{">" * 20} Guessed Countries  | {guessed_country } {"<" * 20}")
        print(f"{">" * 20} Score {score} {"<" * 20}")
        print(f"{">" * 20} Remaining life {life - wrong_guess} {"<" * 20}")
        print(f"{">" * 20} Wrong guesses {wrong_guess} {"<" * 20}")
    print("End Lives")
    # adding score to scores.csv file
    add_score(username, score)


# Main menu function
def main_menu():
    print(f"{">" * 20} Welcome to Vocabulary Builder {"<" * 20}")
    print("1: Word Guessing Game")
    print("2: Definition Matching Game")
    print("3: Country Chain Game")
    print("4: Spell Corrector Game")
    print("5: Exit")

# Main program
def main():
    while True:
        main_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            word_guessing_game()
            break
        elif choice == "2":
            words_definition_game()
            break
        elif choice == "3":
            country_chain_game()
            break
        elif choice == "4":
            spell_corrector()
            break
        elif choice == "5":
            print("Exiting Program")
            break
        else:
            print("Invalid choice. Please try again.")



# Starting the  program from here
while True:
    # make sure user enter 1 or 2 as input

    is_login = input(f"{">" * 20} Register or Login {"<" * 20} \n1: Register \n2: Login  \n")
    if is_login == "1" or is_login == "2":
        break
    else:
        print("Invalid Input Please Try again ")


count_try = 0

if is_login == "2":
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        try:
            if not login(username, password, users_file):
                print("Login successful!")
                main()
                break
            else:
                count_try += 1
                terminator(count_try)
                print(f"{">" * 20} Invalid credentials {"<" * 20}")
                print(f"{">" * 20} you have {3 - count_try} try s left {"<" * 20}")
        except FileNotFoundError as e:
            print(e)
            break

else:
    while True:
        username = input("Enter username: ")
        input_password = input("Enter a password of length 8 at least 1 special character and 1 number: ")
        if password_validator(input_password):
            password = password_validator(input_password)

            try:
                if not register(username, password, users_file):
                    print("Registered Successful")
                    print("Please Login Again")
                    while True:
                        username = input("Enter username: ")
                        password = input("Enter password: ")
                        if not login(username, password, users_file):
                            print("Login successful!")
                            main()
                            break
                        else:
                            count_try += 1
                            terminator(count_try)
                            print(f"{">" * 20} Invalid credentials {"<" * 20 }")
                            print(f"{">" * 20} you have {3 - count_try} try s left {"<" * 20}")
            except FileNotFoundError as e:
                print(e)
                break

        else:
            print("Invalid password. Password must be at least 8 characters long and contain at least one special character and one digit.")






