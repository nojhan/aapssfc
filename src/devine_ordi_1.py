#encoding: utf-8

# En évitant d'utiliser des variables globales, on n'a plus besoin que de deux
# sections de code : les fonctions et le code. Cette bonne pratique évite
# d'avoir à se rappeler des noms de variables définis ailleurs, qui pourraient
# interférer avec des variables du même nom au sein de la fonction.

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

    # On peut utiliser la valeur renvoyée par une fonction directement, 
    # sans passer par une variable intermédiaire.
    return random.randint(nb_min,nb_max)


def reply( answer, guess, min, max ):
    """Analyse la réponse de l'humain et renvoie vrai si on a trouvé la bonne."""

    # Dans cette fonction, on peut éviter d'utiliser des variables globales,
    # en les passant en arguments ET en renvoyant leurs valeurs modifiées.

    # On peut enchainer les tests dans des "si/sinon".
    # Cela évite de tout tester si une condition s'avère vraie avant les autres.
    if answer == 0:
        # L'algorithme de recherche sera bien plus efficace si, au lieu de 
        # réduire l'interval par pas de 1, on utilise le nombre qu'on a essayé.
        min = guess + 1

    elif answer == 1:
        max = guess - 1

    elif answer == 2:
        print("Enfin !")
        # On peut renvoyer plusieurs valeurs à la fois
        return True,min,max

    else: # Si answer n'est pas égale à l'une des valeurs précédentes
        print("Tu dois répondre par 0, 1 ou 2 !")

    # Il est inutile de répéter trois fois cette instruction,
    # en la placant après les tests, on ne passera ici que si aucune instruction
    # "return" n'a été rencontrée
    return False,min,max


########
# Code #
########

import random

min = 0
max = 10
print("Pense à un nombre entre",min,"et",max)

attempts = 10

while attempts > 0:
    guess = try_to_guess(min,max)

    print("Je crois que tu penses au nombre",guess,", est-il:")
    print("0: trop petit ?")
    print("1: trop grand ?")
    print("2: le bon numéro ?")
    answer = int( input() )

    found,min,max = reply( answer, guess, min, max )
    # "False" et "True" sont des mots-clefs du langage,
    # à ne pas confondre avec des chaînes de caractères ou des variables.
    if found == True:
        break
    else:
        attempts = attempts - 1

# Comme la valeur de la variable "found" est un mot-clef (True ou False), 
# on peut écrire le test de manière plus concise.
if found:
    print("J'ai gagné :-)")
else:
    print("J'ai perdu :-(")

