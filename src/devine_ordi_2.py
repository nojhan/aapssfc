#encoding: utf-8


#############
# Fonctions #
#############

import random

def try_to_guess( nb_min, nb_max ):
    """Choisi un nombre compris entre un min et un max et le renvoie."""

    if nb_min == nb_max or nb_min > nb_max:
        # Au cas où cette erreur apparait, il est préférable de signaler l'erreur
        # pour qu'elle puisse être traitée
        raise Exception("tu as triché !")
        

    # Il est plus efficace d'essayer le nombre au milieu des deux bornes,
    # plutôt que d'en choisir un au hasard
    #return nb_min + floor( (nb_max - nb_min) / 2 )

    # En python, il existe un opérateur plus concis
    return nb_min + (nb_max - nb_min) // 2

    # Il aurait été plus concis d'écrire le calcul sous cette forme,
    # mais attention au dépassement avec des grands nombres !
    #return (nb_min + nb_max) / 2


def reply( answer, guess, min, max ):
    """Analyse la réponse de l'humain et renvoie vrai si on a trouvé la bonne."""

    if answer == 0:
        min = guess + 1

    elif answer == 1:
        max = guess - 1

    elif answer == 2:
        print("Enfin !")
        return True,min,max

    else:
        print("Tu dois répondre par 0, 1 ou 2 !")

    return False,min,max


########
# Code #
########

min = 0
max = 10
print("Pense à un nombre entre",min,"et",max)

attempts = 10
found = False

while attempts > 0:
    # Au cas où la fonction try_to_guess fait remonter une erreur,
    # on peut l'attraper ici, afficher un message et sortir.
    try:
        guess = try_to_guess(min,max)
    except Exception as err:
        print("Erreur :",err)
        break

    print("Je crois que tu penses au nombre", guess, ", est-il:")
    print("0: trop petit ?")
    print("1: trop grand ?")
    print("2: le bon numéro ?")
    answer = int( input() )

    found,min,max = reply( answer, guess, min, max )
    if found == True:
        break
    else:
        attempts = attempts - 1

if found:
    print("J'ai gagné :-)")
else:
    print("J'ai perdu :-(")

