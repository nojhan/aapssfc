
import random

import pendu_humain as pendu
import pendu_ordi_1 as AI

def auto_play( secret_word, words ):
    used_letters = set()
    fails = 0
    partial_word = "_" * len(secret_word)
    
    while fails < len( pendu.BOARDS_PIC ):
        words = AI.compatible_words( words, partial_word, used_letters )
 
        if len( words ) == 1:
            return secret_word == words[0]

        elif len(words) == 0:
            return False

        letter = AI.guess_letter_frequency( words, used_letters, False )
        used_letters.add( letter )
        
        if letter in secret_word:
            partial_word = pendu.process( letter, partial_word, secret_word )
        else:
            fails += 1
  
        if fails == len(pendu.BOARDS_PIC) and len(words) > 1:
            return secret_word == random.choice(words)
        
        if "_" not in partial_word:
            return True

    return False


if __name__=="__main__":

    games = 100

    all_words = pendu.download_dic( "http://nojhan.net/aapssfc/data/french_dictionary.utf8" )

    all_played = 0
    all_won = 0
    lost_on = []

    # Essais des mots de tailles variables
    for word_size in range(1,20):
        words = pendu.filter_wordsize( all_words, word_size )
        print(len(words),"mots de taille",word_size,"...")
        
        # Joue sur quelques mots tirés au hasard
        played = 0
        won = 0
        for r in range(games):
            secret_word = random.choice( words )
            if auto_play( secret_word, words ):
                won += 1
            else:
                lost_on.append( secret_word )
            played += 1

        print("\tvictoires :",won,"/",played)
        all_won += won
        all_played += played

    print("Probabilité de gagner :",all_won/float(all_played))
    if len(lost_on) > 0:
        print("Perte sur les mots :\n",", ".join(lost_on))

    # Exercice : essayer tous les mots de chaques tailles
    # et estimer ainsi la probabilité réelle de gagner

