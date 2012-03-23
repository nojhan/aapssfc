
import random

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


def compatible_words( words, partial_word ):
    """ Filtre une liste de mots en ne gardant que les mots compatibles avec un mot partiel """
    compatibles = []
    for word in words:
        if is_compatible( word, partial_word ):
            compatibles.append( word )

    return compatibles


def letters_in( words ):
    letters = set()
    for word in words:
        for letter in word:
            letters.add(letter)
    return letters


def guess_letter( available_letters ):
     # Enlève et retourne une lettre 
    return available_letters.pop()


def guess_letter_random( available_letters ):
    # Converti le set en list...
    letters = list( available_letters )
    # ... afin de pouvoir y tirer un élément au hasard.
    letter = random.choice( letters )
    # Répercuter le changement sur les lettres disponibles.
    available_letters.remove( letter )
    return letter


def guess_letter_random_vowels( available_letters ):
    # Les accents comptent comme des lettres différentes !
    vowels = set( ['a','e','i','o','u','y','é','è','à','ù','ë','ê','â','ï'] )
    
    # Lettres présentes à la fois dans les voyelles ET les lettres disponibles
    available_vowels = available_letters & vowels

    # S'il y a au moins une voyelle dans les lettres disponibles
    if len( available_vowels ) > 0:
        # Les tirer en priorité
        available_letters = available_vowels

    letters = list( available_letters )
    letter = random.choice( letters )
    available_letters.remove( letter )
    return letter


if __name__=="__main__":

    print("Entrez le nombre de lettres de votre mot")
    word_size = int( input() )

    used_letters = set()
    partial_word = "_" * word_size
    fails = 0
    
    words = pendu.filter_wordsize( pendu.download_dic( "http://nojhan.net/aapssfc/data/french_dictionary.utf8" ), word_size )

    while fails < len( pendu.BOARDS_PIC ):
        pendu.display( pendu.BOARDS_PIC, partial_word, fails )
        
        words = compatible_words( words, partial_word )
        print(len(words),"mots compatibles")
        
        # Construit la liste des lettres existantes dans les mots restants.
        remaining_letters = letters_in( words )

        # Ne garde que les lettres n'ayant pas déjà été utilisées
        remaining_letters = remaining_letters - used_letters
        print(len(remaining_letters),"lettres restantes")

        letter = guess_letter_random_vowels( remaining_letters )
        used_letters.add( letter )
        print("Je pense à la lettre : «",letter,"», est-elle présente dans le mot ? [o/n]")
        answer = input()
        answer.lower()

        if answer == "n":
            fails += 1
            continue
        else:
            is_correct = False
            while not is_correct:
                print("Entrez le nouveau mot partiel :")
                new_word = input()
                new_word = new_word.lower()
                
                print("«",new_word,"», est-ce correct ? [o/n]")
                answer = input()

                if len(new_word) != len(partial_word):
                    print("Le nombre de lettres ne correspond pas !")
                    is_correct = False
                    continue
                
                if answer.lower() == "o":
                    is_correct = True

                # Ici, on aurait put écrire :
                #    continue
                #else:
                #    break
                # mais cela aurait été inutile !

            partial_word = new_word
    
            if "_" not in partial_word:
                break

    if fails >= len( pendu.BOARDS_PIC ):
        print("J'ai perdu :-(")
    else:
        print("J'ai gagné :-)")
