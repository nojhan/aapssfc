#encoding: utf-8

import random

class Mastermind():
    
    def __init__(self, slots = 4, colors = [0, 1, 2, 3, 4] ):
        #self.colors = { 0:"rouge", 1:"jaune", 2:"vert", 3:"bleu", 4:"orange", 5:"blanc", 6:"violet", 7:"fuchsia"}
        self.colors = [i for i in range(8)]
        self.slots = slots


    def random_code(self):
        code = []
        for s in range(self.slots):
            code.append( random.randrange( len(self.colors) ) )
        return code


    def feedback(self, code, secret_code ):
        assert( len(code) == len(secret_code) )
        good_positions = 0
        good_colors = 0
        for i in range(len(code)):
            # Si la couleur est à la bonne position
            if code[i] == secret_code[i]:
                good_positions += 1
            # Si la couleur n'est pas à cette position, mais qu'elle existe ailleurs
            elif code[i] in secret_code[:i]+secret_code[i+1:]:
                good_colors += 1

        return good_positions, good_colors


    def ask_code(self):
        print("Entrez votre code")
        str_code = str(input())
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
    
