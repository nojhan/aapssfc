#encoding: utf-8

import random

min=0
max=10
print("Pense à un nombre entre",min,"et",max)

essais = 4

def deviner(nb_min,nb_max):
    if nb_min == nb_max or nb_min > nb_max:
        print("Tu as triché !")
    hasard = random.randint(nb_min,nb_max)
    return hasard


def repondu( reponse ):
    if reponse == 0:
        min = min + 1
        return False

    elif reponse == 1:
        max = max - 1
        return False

    elif reponse == 2:
        print("Enfin !")
        return True

    else:
        print("Tu dois répondre par 1, 2 ou 3 !")
        return False


while essais > 0:
    devine = deviner(min,max)

    print("Je pense au nombre",devine,", est-il:")
    print("0: trop petit ?")
    print("1: trop grand ?")
    print("2: le bon numéro ?")
    reponse = int( input() )

    trouve = repondu( reponse )
    if trouve == True:
        break

