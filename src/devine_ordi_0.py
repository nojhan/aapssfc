#encoding: utf-8

import random

min=0
max=10
print("Pense à un nombre entre",min,"et",max)

essais = 4

def devine_entre(nb_min,nb_max):
    if nb_min == nb_max:
        print("Tu as triché !")
    return random.randint(nb_min,nb_max)


while essais > 0:
    devine = devine_entre(min,max)

    print("Je pense au nombre",devine,", est-il:")
    print("0: trop petit ?")
    print("1: trop grand ?")
    print("2: le bon numéro ?")
    reponse = int( input() )

    if reponse == 0:
        min = min + 1

    elif reponse == 1:
        max = max - 1

    elif reponse == 2:
        print("Enfin !")
        break

    else:
        print("Tu dois répondre par 1, 2 ou 3 !")

    
