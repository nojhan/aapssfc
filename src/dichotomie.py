#encoding: utf-8

def search(value, tab):
    """ Cherche une valeur donnée au sein d'une liste d'entiers triée par ordre croissant """

    vmin = 0
    vmax = len(tab)

    # La recherche est terminée si la valeur min est supérieure à la valeur max.
    while vmin <= vmax:
        mid = vmin + (vmax - vmin) // 2;
        
        # Si la valeur courante est inférieur à l'élément central, 
        # reserrer la recherche.
        if value < tab[mid]:
            vmax = mid - 1;
        
        # Si la valeur est supérieure aussi.
        elif value > tab[mid]:
            vmin = mid + 1;
        
        # Sinon, c'est qu'on a trouvé.
        else:
            return mid;
    
    # Si on arrive ici, l'élément n'est pas dans la liste
    return -1


if __name__ == "__main__":

    import random

    size = 50
    # Construire une liste d'entiers croissants en prenant 75% des valeurs.
    t = [n for n in range(size) if random.random() < 0.75]
    # Tirer au hasard une valeur à chercher.
    v = random.randint(0,size-1)
    
    print(t)
    print("L'élément", v, "...")
    
    pos = search(v,t)
    if pos == -1:
        print("... n'a pas été trouvé dans la liste")
    else:
        print("... est à la position", pos )

