#encoding: utf-8
import random
from urllib.request import urlopen

BOARDS_PIC = [
"""
 ╒══╗
 │  ║
    ║
    ║
    ║
════╩═
""",
"""
 ╒══╗
 │  ║
 ☹  ║
    ║
    ║
════╩═
""",
"""
 ╒══╗
 │  ║
 ☹  ║
 │  ║
    ║
════╩═
""",
"""
 ╒══╗
 │  ║
 ☹  ║
/│  ║
    ║
════╩═
""",
"""
 ╒══╗
 │  ║
 ☹  ║
/│\ ║
    ║
════╩═
""",
"""
 ╒══╗
 │  ║
 ☹  ║
/│\ ║
╱   ║
════╩═
""",
"""
 ╒══╗
 │  ║
 ☹  ║
/│\ ║
╱ ╲ ║
════╩═
"""]


def download_dic( url ):
    """ Télécharge une liste de mots """
    # Ouvre la page web, fait quelque chose avec puis la ferme automatiquement
    with urlopen( url ) as page:
        # Renvoie le contenu de la page, sous forme d'une liste de mots
        return page.read().split()


def filter_wordsize( words, word_size = 3 ):
    """ Décode en unicode chaque mot dans words
        ssi la longueur du mot est celle demandée """
    return [w.decode("utf-8") for w in words if len(w) == word_size ]


def pick_word( words ):
    """ Renvoi un mot choisi au hasard dans une liste """
    return words[ random.randrange( len(words) ) ]


def display( boards, partial_word, fails ):
    """ Affiche l'état du pendu et le mot deviné """
    print( boards[fails] )
    print( "« " + partial_word + " »" )


def process( letter, partial_word, secret_word ):
    """ Insère les lettres devinées dans le mot en cours """
    for i in range(len(secret_word)):
        if secret_word[i] == letter:
            # En python, les chaines de caractères sont "immutable", 
            # c'est à dire qu'on ne peut pas écrire :
            #     partial_word[i] = letter
            # Pour faire la même chose, il faut réaffecter un nouveau contenu à la variable.
            # On concatène donc la partie à gauche de la lettre avec la partie à droite.
            partial_word = partial_word[:i] + letter + partial_word[i+1:]
    return partial_word


def play( secret_word ):
    """ Boucle de jeu principale, renvoie vrai si le joueur a gagné """
    partial_word = "_" * len(secret_word)
    fails = 0
    used_letter = ""
    while fails < len( BOARDS_PIC ):
        display( BOARDS_PIC, partial_word, fails )

        print("À quelle lettre pensez-vous ?")
        letter = input()
        # Les majuscules étant considérés par python comme différentes des minuscules,
        # on évite des problèmes en convertissant tout en minuscule.
        letter = letter.lower()

        # Il est possible de soumettre le mot entier.
        if letter == secret_word:
            return True

        if letter in used_letter:
            print("Vous avez déjà essayé les lettres suivantes :",used_letter)
            # Aller directement à l'itération suivante, sans compter les ratés.
            continue
        else:
            used_letter += letter

        if letter in secret_word:
            partial_word = process( letter, partial_word, secret_word )
        else:
            fails = fails + 1

        # S'il n'y a pas de caractère "_" dans le mot, c'est qu'il y a victoire.
        if "_" not in partial_word:
            return True

    # On a épuisé tous les essais, c'est perdu.
    return False


if __name__=="__main__":
    word_size = 8
    words = filter_wordsize( download_dic( "http://nojhan.net/aapssfc/data/french_dictionary.utf8" ), word_size )
    print( len(words),"mots dans le dictionaire" )
    
    secret_word = pick_word( words )
    #print( secret_word )

    won = play( secret_word )

    if won:
        print("Gagné :-)")
    else:
        print("Perdu :-(")
        print("Le mot était : ",secret_word )

