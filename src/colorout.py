#!/usr/bin/env python3
#encoding: utf-8

############################################################################################
# Ce script permet de colorier chaque occurence d'un pattern provenant de l'entrée standard.
# Exemples d'utilisation:
#    cat colorout.py | colorout color red bold
#    colorout /home/[a-z]+ magenta < /etc/passwd
#    ls -l | colorout .\(r.-\){3} yellow standard
#    make 2>&1 | colorout [0-9]+ green | colorout error
#    make 2>&1 | colorout [0-9]+ yellow standard | colorout error | colorout warning magenta | colorout \(note\)\|\(#pragma\\s+\) green standard
############################################################################################

import re

styles = {"standard":0, "bold":1, "reverse":2}
colors = {"black":30, "red":31, "green":32, "yellow":33, "blue":34, "magenta":35, "cyan":36, "white":37}

def colored( text, pattern, color, style = "standard" ):
    """Formatte chaque occurence de l'expression régulière 'pattern' dans 'text' avec la couleur et le style indiqué,
       en utilisant les séquences d'échappement ANSI appropriés."""

    # Caractères spéciaux.
    start = "\033["
    stop = "\033[0m"

    # Conversion en string du code couleur demandé.
    cs = str(styles[style])
    cc = str(colors[color])

    # Compilation de l'expression régulière.
    regex = re.compile(pattern, re.IGNORECASE)

    # Texte colorié.
    ctext = ""
    e = 0
    # Pour chaque occurence d'une correspondance dans le texte.
    for match in regex.finditer(text):

        # Position dans text du début de l'occurence.
        s = match.start()

        # On ajoute le texte entre la dernière occurence,,
        # il faut noter que e=0, à la première itération.
        ctext += text[e:s]
        
        # Position dans text de la fin de l'occurence.
        e = match.end()

        # On ajoute l'occurence, en colorant.
        ctext += start + cs + ";" + cc + "m" + text[s:e] + stop
    
    # On ajoute la fin du texte.
    ctext += text[e:]

    return ctext


if __name__ == "__main__":
    import sys

    pattern = ".*"
    color= "red"
    style = "bold"

    nargs = len(sys.argv)

    if nargs <= 1 or nargs >= 5:
        msg = "Usage: colorout pattern [color] [style]"
        msg += "\n\tAvailable colors: "+" ".join(colors)
        msg += "\n\tAvailable styles: "+" ".join(styles)
        sys.exit(msg)
    else:
        if nargs > 1:
             pattern = sys.argv[1]
        if nargs > 2:
            color = sys.argv[2]
        if nargs > 3:
            style = sys.argv[3]

    for line in sys.stdin:
        print( colored( line, pattern, color, style ), end="" )

