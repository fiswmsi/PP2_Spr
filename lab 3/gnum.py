#13
import random

def guess_the_number():
    print("Hello! What is your name?")
    name = input()

    randnum = random.randint(1, 20)
    cnt = 0

    print(f"\nWell, {name}, I am thinking of a number between 1 and 20.")

    while True:
        print("Take a guess.")
        guess = int(input())
        cnt += 1

        if guess < randnum:
            print("Your guess is too low.")
        elif guess > randnum:
            print("Your guess is too high.")
        else:
            print(f"Good job, {name}! You guessed my number in {cnt} guesses!")
            break

guess_the_number()