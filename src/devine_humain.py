#encoding: utf-8

import random

min=0
max=10
print("Je pense à un nombre entre", min, "et", max )

# Tire un entier ("integer") au hasard entre min et max compris
number = random.randint(min,max)

attempts = 4

while attempts > 0:
    print("guess ? ")

    # attends une saisie de l'utilisateur sous forme de chaine de caractère
    guess = input()

    # interprète la chaine de caractère comme un entier
    guess = int(guess)

    if guess > number:
        print("Trop grand")

    if guess < number:
        print("Trop petit")

    if guess == number:
        # sort directement de la boucle "while"
        break

    attempts = attempts - 1
    print("Plus que", attempts, "essais")


# On arrive ici dans deux situations :
# 1) tous les essais ont été tentés, la boucle s'arrête d'elle-même
# 2) on a deviné le nombre secret, on est sorti par l'instruction "break"

if guess != number:
    print("Perdu, je pensais au nombre", number)
else:
    print("Bravo !")

