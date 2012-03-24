import random


def swap( items, i, j ):
    assert( i < len(items) and j < len(items) )
    items[i], items[j] = items[j],items[i]
    return items


def permute( items, index ):
    """ Permute 4 chiffres deux à deux, par exemple avec index==0 :
0 1 2 3 4 5 6 7
▲ ▲ ▲ ▲ 
│ └─┘ │
└─────┘
3 2 1 0 4 5 6 7
"""
    assert( index+3 < len(items) )

    # Échange les nombres aux deux bouts.
    items = swap( items, index, index+3 )

    # Échange les nombres au milieu.
    items = swap( items, index+1, index+2 )

    return items


def display_items( items ):
    print(" ".join([str(i) for i in items]))


def display_permutation( index ):
    pad = "  " * i
    print( pad + ("▲ " * 4) )
    print( pad + "│ └─┘ │" )
    print( pad + "└─────┘" )
    

def shuffle( items, permutations ):
    for n in range(permutations):
        i = random.randint(0,size-4)
        items = permute( items, i )


if __name__=="__main__":
    size = 8
    nb_shuffle = 5

    items = [n for n in range(size)]
    items_ok = [n for n in range(size)]

    shuffle( items, nb_shuffle )
    print("Séquence mélangée en",nb_shuffle,"permutations")
    display_items( items )

    attempts = 1
    while True:
        print("Quelle permutation ?")
        i = int( input() )
        if 0 > i or i > size-4:
            print("L'index doit être compris entre 0 et",size-4)
        else:
            display_items( items )
            permute( items, i )
            display_permutation( i )
            display_items( items )
            
            if items == items_ok:
                print("Vous avez réussi en",attempts,"permutations")
                break
            else:
                attempts += 1

