#encoding: utf-8

# Le code se découpe en deux parties :
# dans la première, on met en place les variables de base
# dans la seconde, on défini des _fonctions_
# dans la troisième, on les instructions qui les utilisent

#############
# Variables #
#############

import random

min=0
max=10
print("Pense à un nombre entre",min,"et",max)

attempts = 10


#############
# Fonctions #
#############

def try_to_guess(nb_min,nb_max):
    """Choisi un nombre compris entre un min et un max et le renvoie."""

    # On peut combiner deux conditions à l'aide d'opérateurs logiques.
    # Ce test sert à vérifier s'il n'y a pas eu d'erreurs dans l'enchaînement
    # des réponses de l'être humain.
    # Si le min est le même que le max, il n'y a pas d'entier possible entre les deux.
    # De même, si le min est supérieur au max, il y a eu erreur de logique.
    if nb_min == nb_max or nb_min > nb_max:
        print("Tu as triché !")

    rand = random.randint(nb_min,nb_max)
    # Le nombre tiré au hasard est _renvoyé_
    return rand


def reply( answer ):
    """Analyse la réponse de l'humain et renvoie vrai si on a trouvé la bonne."""

    # Ces variables ont été définies en dehors de la fonction, elles sont "globales"
    # il est nécessaire de le spécifier explicitement
    global min,max

    if answer == 0:
        min = min + 1
        return False

    elif answer == 1:
        max = max - 1
        return False

    elif answer == 2:
        print("Enfin !")
        return True

    else:
        print("Tu dois répondre par 1, 2 ou 3 !")
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
    answer = int( input() )

    found = reply( answer )
    if found == True:
        # il est inutile de continuer si on a déjà trouvé
        break
    else:
        attempts = attempts - 1

if found == True:
    print("J'ai gagné :-)")
else:
    print("J'ai perdu :-(")

