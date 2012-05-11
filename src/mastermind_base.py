#encoding: utf-8

import random

class Mastermind():

    def __init__(self, slots = 4, colors = [i for i in range(8)] ):
        """Initialise le plateau avec un nombre de cases et de couleurs donnés par l'utilisateur."""
        self.colors = colors
        self.slots = slots


    def random_code(self):
        """Tire au hasard un code à faire deviner."""
        # Choisir au hasard un élément dans "colors" pour chaque nombre entier entre 0 et "slots"
        return [ random.choice(self.colors) for i in range(self.slots) ]


    def feedback(self, code, secret_code ):
        """Décompte les couleurs existantes dans le code secret"""
        # Le code passé doit avoir le même nombre de chiffres que le code secret,
        # sinon, il y a vraiment un problème.
        assert( len(code) == len(secret_code) )

        good_positions = 0
        good_colors = 0
        for i in range(len(code)):
            # Si la couleur est à la bonne position
            if code[i] == secret_code[i]:
                good_positions += 1
            # Si la couleur n'est pas à cette position, mais qu'elle existe ailleurs:
            # == si le code est dans la concaténation des chiffres avant le chiffre vérifié et de ceux après
            elif code[i] in secret_code[:i]+secret_code[i+1:]:
                good_colors += 1

        return good_positions, good_colors


    def ask_code(self):
        print("Entrez votre code (4 chiffres entre 0 et 7)")
        # On s'attends à une série de chiffres accolés,
        # on s'assure donc de considérer l'entrée comme une chaine de caractères…
        str_code = str(input())

        # … sur lesquels on pourra itérer, en les interprétants comme des entiers.
        code = [int(i) for i in str_code]

        return code


    def display(self, code, good_positions, good_colors ):
        #print("".join([str(c) for c in code]))
        print(good_positions,"à la bonne position,",good_colors,"mal placés")


    def play(self, maxtry = 12 ):
        secret_code = self.random_code()
        print(secret_code)

        fails = 0
        while fails < maxtry:
            fails += 1

            code = self.ask_code()

            if code == secret_code:
                break
            else:
                gp,gc = self.feedback( code, secret_code )
                self.display(code,gp,gc)

        if code == secret_code:
            return True,fails
        else:
            return False,fails


if __name__=="__main__":
    maxtry = 12

    m = Mastermind()
    won,tries = m.play( maxtry )

    if won:
        print("Vous avez gagné en",tries,"essais")
    else:
        print("Vous avez perdu après",tries,"essais")
    
