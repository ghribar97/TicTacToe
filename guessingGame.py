import random


def play():
    guessesTaken = 0
    print('Hello! What is your name?')
    myName = input()
    number = random.randint(1, 100)
    print('Well, ' + myName + ', I am thinking of a number between 1 and 100.')
    while guessesTaken < 30:
        print('Take a guess.')
        guess = input()
        try:
            guess = int(guess)
        except TypeError:
            exit(0)
        except ValueError:
            exit(0)
        guessesTaken = guessesTaken + 1
        if guess < number:
            print('Your guess is too low.')
        if guess > number:
            print('Your guess is too high.')
        if guess == number:
            break
    if guess == number:
        guessesTaken = str(guessesTaken)
        print('Good job, ' + myName + '! You guessed my number in ' + guessesTaken + ' guesses!')
    else:
        number = str(number)
        print('Nope. The number I was thinking of was ' + number)
    exit(0)