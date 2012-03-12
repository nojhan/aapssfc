#encoding: utf-8

import random

min=0
max=10
print("Je pense à un nombre entre", min, "et", max )

nombre = random.randint(min,max)
essais=4

while essais > 0:
    print("Devine ? ")
    devine = input()
    devine = int(devine)

    if devine > nombre:
        print("Trop grand")

    if devine < nombre:
        print("Trop petit")

    if devine == nombre:
        break

    essais = essais - 1
    print("Plus que", essais, "essais")


if devine != nombre:
    print("Perdu, je pensais au nombre", nombre)
else:
    print("Bravo !")

