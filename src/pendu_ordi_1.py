
import random
import operator

import pendu_humain as pendu

def is_compatible( word, partial_word ):
    """ Teste si un mot complet est compatible avec un mot partiel.
        Par exemple :
        >>> from pendu_ordi import *
        >>> is_compatible("hirondelle","_a____e__e")
        False
        >>> is_compatible("hirondelle","______e__e")
        True
    """
    if len(word) != len(partial_word):
        return False

    for i in range(len(word)):
        if partial_word[i] == "_":
            continue

        elif word[i] != partial_word[i]:
            return False
    
    return True


def compatible_words( words, partial_word, used_letters ):
    """ Filtre une liste de mots en ne gardant que les mots compatibles avec un mot partiel """
    compatibles = []
    for word in words:
        # Ensemble des lettres utilisées dans le mot
        word_letters = set(word)
        # Les lettres disponibles sont celles qui ont été utilisées MOINS celles déjà devinées
        false_letters = used_letters - set(partial_word.replace("_",""))

        # Si le mot est compatible ET qu'aucune des lettres utilisées n'y est 
        if is_compatible( word, partial_word ) and len( false_letters & word_letters ) == 0:
            compatibles.append( word )

    return compatibles


def guess_letter_frequency( words, used_letters, verbose = True ):
    """ Choisi une lettre en fonction de sa fréquence dans la liste des mots compatibles disponibles """
    freqs = {}
    for word in words:
        for letter in word:
            if letter not in used_letters:
                # Si la lettre n'a pas déjà été rencontrée.
                if letter not in freqs:
                    # Créer la clef correspondante dans le dictionnaire.
                    freqs[letter] = 1
                else:
                    # Incrémenter le compteur d'occurence.
                    freqs[letter] += 1

    best_letter = best_letter_0( freqs )
    if verbose:
        print("Lettre la plus probable : «",best_letter,"» avec",freqs[best_letter],"occurences")
    return best_letter


def best_letter_0( freqs ):
    # Première clef dans le dictionnaire
    best_letter = list(freqs.keys())[0]
    for letter in freqs:
        if freqs[letter] > freqs[best_letter]:
            best_letter = letter
    return best_letter


def best_letter_1( freqs ):
    # On pourrait aussi trier les clefs du dictionnaire selon la valeur des éléments associés
    sorted_letters = sorted( freqs.items(), key=operator.itemgetter(1) )
    # Une fois triés par ordre croissant, la lettre la plus probable est en dernière
    best_letter = sorted_letters[-1][0]
    return best_letter


def ask_correct():
    print("Est-ce correct ? [o/n]")
    answer = input()
    answer = answer.lower()

    if answer == 'o':
        return True
    else:
        return False


def ask_partial_word( partial_word ):
    is_correct = False
    while not is_correct:
        print("Entrez le nouveau mot partiel :")
        new_word = input()
        new_word = new_word.lower()
        
        print("«",new_word,"»")
        is_correct = ask_correct()

        if len(new_word) != len(partial_word):
            print("Le nombre de lettres ne correspond pas !")
            is_correct = False

    return new_word


def play( partial_word, words ):
    used_letters = set()
    fails = 0
    
    while fails < len( pendu.BOARDS_PIC ):
        pendu.display( pendu.BOARDS_PIC, partial_word, fails )
        
        words = compatible_words( words, partial_word, used_letters )
        print(len(words),"mots compatibles")
 
        # S'il ne reste qu'un mot à tester,
        if len( words ) == 1:
            # on le propose directement.
            print("Je pense au mot «",words[0],"»")
            return ask_correct()

        elif len(words) == 0:
            print("Je ne connais pas ce mot.")
            return False

        letter = guess_letter_frequency( words, used_letters )
        used_letters.add( letter )
        print("Je pense à la lettre : «",letter,"»")
        
        if ask_correct():
            partial_word = ask_partial_word( partial_word )
        else:
            fails += 1
  
        # Si c'est la dernière chance mais qu'il reste trop de mots à tester
        if fails == len(pendu.BOARDS_PIC) and len(words) > 1:
            # on tente au hasard
            print("Je pense au mot «",random.choice(words),"»")
            return ask_correct()
        
        if "_" not in partial_word:
            return True

    return False


if __name__=="__main__":

    print("Entrez votre mot secret")
    word_size = len( input() )
    partial_word = "_" * word_size

    words = pendu.filter_wordsize( pendu.download_dic( "http://nojhan.net/aapssfc/data/french_dictionary.utf8" ), word_size )
    
    won = play( partial_word, words )

    if won:
        print("J'ai gagné :-)")
    else:
        print("J'ai perdu :-(")
