#encoding: utf-8

import random

def play( swap, verbose = True ):
    """ Joue une partie du jeu de Mounty Hall et renvoie vrai si la partie est gagnée """

    wins = 0
    doors = ["chèvre","chèvre","voiture"]
    random.shuffle(doors)
    chosen_door = random.randrange( len(doors) )

    if verbose:
        print("Le joueur choisi la porte",chosen_door)

    for i in range(len(doors)):
        if doors[i] == "chèvre" and i != chosen_door:
            goat_door = i
            if verbose:
                print("\tLe présentateur ouvre la porte",goat_door)
            break

    if swap:
        for i in range(len(doors)):
            if i != goat_door and i != chosen_door:
                chosen_door = i
                if verbose:
                    print("\tLe joueur choisi de changer pour la porte",chosen_door)
                break
    
    if doors[chosen_door] == "voiture":
        if verbose:
            print("\tLe joueur gagne la voiture")
        wins = wins + 1
    else:
        if verbose:
            print("\tLe joueur perd et garde la chèvre")

    return wins


if __name__ == "__main__":
    verbose = False
    runs = 100000
    wins_swap = 0
    wins_noswap = 0
    for i in range(runs):
        wins_noswap += play( False, verbose )
        wins_swap += play( True, verbose )

    print("Probabilité de gagner la voiture en changeant",wins_swap/runs,"et sans changer",wins_noswap/runs)

