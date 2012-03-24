#encoding: utf-8

import random
import curses
import time


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


def display( scr, items, index, msg = "" ):
    """ Affiche un écran de jeu interactif en mode texte:
D'abord une ligne pour un éventuel message,
ensuite la séquence permutée,
puis le schéma de permutation.

Par exemple:
Séquence mélangée en 2 permutations
0 1 6 7 3 2 5 4
▲ ▲ ▲ ▲
│ └─┘ │
└─────┘
"""
    # Efface ce qui aurait été affiché précédemment.
    scr.clear()
    # Ajoute une chaine de caractères,
    # à partir de la première ligne et de la première colonne.
    scr.addstr( 0,0, msg + "\n" )
    # Rempli le restant de la ligne affichée à l'écran par des espaces.
    # (lire "CLeaR TO End Of Line")
    scr.clrtoeol()

    # On peut omettre les coordonnées, le curseur d'affichage part alors de la 
    # dernière position...
    scr.addstr( " ".join([str(i) for i in items]) )
    # ... d'où l'intérêt d'ajouter des fins de ligne (caractère "\n").
    scr.addstr("\n")

    # On insèrera une colonne d'espaces avant le schéma de permutation, 
    # selon l'index considéré.
    pad = "  " * index

    scr.addstr( pad + ("▲ " * 4) + "\n" )
    scr.clrtoeol()
    scr.addstr( pad + "│ └─┘ │\n" )
    scr.clrtoeol()
    scr.addstr( pad + "└─────┘\n" )
    scr.clrtoeol()
    
    # Rempli l'écran de ligne vide jusqu'en bas ("CLeaR TO BOttom").
    scr.clrtobot()


def shuffle( items, permutations ):
    """ Applique un nombre donné de permutations aléatoires """
    for n in range(permutations):
        i = random.randint(0,size-4)
        items = permute( items, i )


def loop( scr, items, nb_shuffle ):
    msg = "Séquence mélangée en "+str(nb_shuffle)+" permutations"
    display( scr, items, 0, msg )
    
    end_msg = ""

    ui_delay = 0.05
    # Modèle de la séquence initiale, ordonnée
    items_ok = sorted( items )
    attempts = 1
    i = 0
    while True:
        # Récupère le code de la touche qui viens d'être utilisée.
        keycode = scr.getch()
        cmd = chr(0)

        # Si le code est un caractère ASCII (une lettre non accentuée)
        if 0 < keycode < 256:
            # Récupère le caractère correspondant à ce code.
            cmd = chr(keycode)

        if cmd in 'qQ':
            break

        elif keycode == curses.KEY_LEFT:
            if i > 0:
                i -= 1

        elif keycode == curses.KEY_RIGHT:
            if i < size-4:
                i += 1

        elif cmd == " " or keycode == curses.KEY_UP:
            permute( items, i )
            
            # Si la séquence permutée correspond à la même séquence, mais triée 
            if items == items_ok:
                msg = "Vous avez réussi en "+str(attempts)+" permutations"
                end_msg = msg
            else:
                attempts += 1

        # Affiche l'écran de jeu
        display( scr, items, i, msg )
        # Met à jour le terminal
        scr.refresh()
        # Attends quelques millisecondes avant de relancer le tout.
        # Si on n'attends pas, le processeur sera utilisé à 100%, 
        # ce qui est inutile vu le temps de réaction moyen d'un être humain.
        time.sleep( ui_delay )

    return end_msg


def play( size, nb_shuffle ):
    
    scr = curses.initscr()
    # Ne pas afficher les touches pressées.
    curses.noecho()
    # Active la prise en compte des touches "flèches".
    scr.keypad(1)

    items = [n for n in range(size)]

    end_msg = ""
    try:
        shuffle( items, nb_shuffle )
        end_msg = loop( scr, items, nb_shuffle )

    # Quelles que soit les erreurs ayant été levées, ou pas, 
    # on effectue ce bloc de code.
    finally:
        # Dé-initialise la bibliothèque et remet le terminal 
        # dans sa configuration précédente, sans quoi le terminal 
        # ne s'affichera plus correctement à la sorti du programme.
        curses.endwin()

    return end_msg


if __name__=="__main__":
    size = 8
    nb_shuffle = 2
    
    msg = play( size, nb_shuffle )

    # Si le message n'est pas vide.
    if msg:
        print(msg)

