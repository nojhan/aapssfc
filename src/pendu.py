#encoding: utf-8

import random
from urllib.request import urlopen

def download_dic( url ):
    with urlopen( url ) as page:
        return page.read().split()


def filter_wordsize( words, word_size = 3 ):
     return [w for w in words if len(w) == word_size ]


def pick_word( words ):
    return words[ random.randrange( len(words) ) ]


if __name__=="__main__":
    word_size = 5
    words = filter_wordsize( download_dic( "http://nojhan.net/aapssfc/data/french_dictionary.utf8" ), word_size )
    print(len(words),"mots dans le dictionaire")
    secret_word = pick_word( words )
    

