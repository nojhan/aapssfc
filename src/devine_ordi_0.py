#encoding: utf-8

# Le code se découpe en deux parties :
# dans la première, on met en place les variables de base
# dans la seconde, on défini des _fonctions_
# dans la troisième, on les instructions qui les utilisent

#############
# Variables #
#############

import random

min = 0
max = 10
print("Pense à un nombre entre",min,"et",max)

attempts = 10


#############
# Fonctions #
#############

def try_to_guess(nb_min,nb_max):
    """Choisi un nombre compris entre un min et un max et le renvoie."""

    if nb_min == nb_max
        print("Tu as triché !")
        
    if nb_min > nb_max:
        print("Tu as triché !")

    rand = random.randint(nb_min,nb_max)
    # Le nombre tiré au hasard est _renvoyé_
    return rand


def reply( answer ):
    """Analyse la réponse de l'humain et renvoie vrai si on a trouvé la bonne."""

    # Ces variables ont été définies en dehors de la fonction, elles sont "globales",
    # il est nécessaire de le spécifier explicitement.
    global min,max

    if answer == 0:
        min = min + 1
        return False

    if answer == 1:
        max = max - 1
        return False

    if answer == 2:
        print("Enfin !")
        return True

    if answer > 2:
        print("Tu dois répondre par 0, 1 ou 2 !")
        return False


########
# Code #
########

while attempts > 0:
    guess = try_to_guess(min,max)

    print("Je crois que tu penses au nombre",guess,", est-il:")
    print("0: trop petit ?")
    print("1: trop grand ?")
    print("2: le bon numéro ?")
    word = input()
    answer = int( word )

    found = reply( answer )
    if found == True:
        # Il est inutile de continuer si on a déjà trouvé.
        break
    else:
        attempts = attempts - 1

if found == True:
    print("J'ai gagné :-)")
else:
    print("J'ai perdu :-(")

