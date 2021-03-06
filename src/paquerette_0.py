#encoding: utf-8

import math

import Image
import ImageDraw
import ImageColor

# Propriétés de la scène
width = 500
perspective = width # Déformation due à la perspective
cameraZ = -width    # Recul de la caméra
zBuffer = {}        # « Calque » pour gérer les points superposés

# Création d'un objet image vide où dessiner
im = Image.new("RGB", (width,width) )
draw = ImageDraw.Draw(im)

#######################
# Fonctions de dessin #
#######################

# Le système de coordonnées utilisé est choisi du point de vue de la caméra :
#     z
#    /
#   +-- x
#   |
#   y


def sphere(a, b, radius):
    """Prend des coordonnées 2D ("a" et "b") entre 0 et 1 et les déforment
    de manière à les placer dans un cercle de rayon "radius".
    Ajoute de la profondeur le long de l'axe b et un gradient de couleur jaune."""

    # Angle en radian (pi/2 = 180°)
    angle = a * math.pi * 2

    # Centre du cercle
    x0 = radius*2
    y0 = radius*2

    return {"x":math.cos(angle) * radius * b + x0, # projection de a vers x
            "y":math.sin(angle) * radius * b + y0 ,# projection de b vers y
            "z": b * radius - radius / 2,          # profondeur le long de b
            "r": 50 + math.floor((1 - b**2) * 300),# gradient de couleur rouge
            "g": 50 + math.floor((1 - b**2) * 200),# gradient de couleur verte
            "b": 0,                                # pas de couleur bleue
            }


def petal(a,b,radius):
    """Prends des coordonnées 2D dans [0,1], les déforment dans un cercle de rayon "radius"
    et ne renvoie que les points compris dans une troncature de ce cercle.
    Ajoute de la profondeur et un gradient de couleur blanche."""

    # Projection de a et b dans x et y
    x = a * radius*2
    y = b * radius*2
    # Centre du cercle
    x0 = radius
    y0 = radius

    # Si la distance entre le centre rayon et le point dessiné est inférieure à la taille du rayon
    if math.sqrt((x - x0) * (x - x0) + (y - y0) * (y - y0)) < radius:
        return {"x": x,
                "y": y * (1 + b) / 2,                # y de plus en plus petit vers le bas
                "z": b * radius - radius / 2,        # Profondeur sphérique
                "r": 100 + math.floor((1 - b) * 155),# Gradient blanc :
                "g": 100 + math.floor((1 - b) * 155),#    toutes les composantes…
                "b": 100 + math.floor((1 - b) * 155) #    … évoluent en fonction de b.
                }
    else:
        # Sinon, on ne veut pas dessiner de point : on ne renvoie rien
        return None


def cylinder( a,b, radius=100, length=400 ):
    """Déforme des coordonnées dans [0,1] en un cylindre de rayon "radius" et de longueur "length".
    Ajoute une profondeur sur b et un gradient vert."""

    angle = a * 2*math.pi

    return {"x": math.cos(angle) * radius,
            "y": math.sin(angle) * radius,
            "z": b * length - length / 2, # le cylindre est centré
            "r": 0,
            "g": math.floor(b*255),
            "b": 0 }


############################################
# Fonctions de manipulation de coordonnées #
############################################

# Les fonctions "rotate_*" déplacent toutes un point "d" selon une rotation d'angle "a", 
# autour d'un axe donné.
# Les « points » sont ici des dictionnaires disposant de clefs "x","y" et "z".

def rotate_x( d, a ):
    """Rotation du point d d'un angle a autour de l'axe x."""
    # Si l'objet "d" existe (c'est à dire s'il n'est pas "None")
    if d:
        # Rotation
        d["y"] = d["y"] * math.cos(a) - d["z"] * math.sin(a)
        d["z"] = d["y"] * math.sin(a) + d["z"] * math.cos(a)
        return d
    else:
        return None


def rotate_y( d, a ):
    """Rotation du point d d'un angle a autour de l'axe y."""
    if d:
        d["z"] = d["z"] * math.cos(a) - d["x"] * math.sin(a)
        d["x"] = d["z"] * math.sin(a) + d["x"] * math.cos(a)
        return d
    else:
        return None


def rotate_z( d, a ):
    """Rotation du point d d'un angle a autour de l'axe z."""
    if d:
        d["x"] = d["x"] * math.cos(a) - d["y"] * math.sin(a)
        d["y"] = d["x"] * math.sin(a) + d["y"] * math.cos(a)
        return d
    else:
        return None


def move( d, dx, dy, dz ):
    """Déplace un point "d" selon des distances données par "dx", "dy" et "dz"."""
    if d:
        # les "d*" peuvent être positifs ou négatifs
        d["x"] = d["x"] + dx
        d["y"] = d["y"] + dy
        d["z"] = d["z"] + dz
        return d
    else:
        return None


def draw_point( point ):
    """Projette un point donné en coordonnées 3D sur une image (2D, par définition)."""

    # Si le point n'est pas en dehors de la forme (ce qui peut arriver si on dessine un pétale).
    if point:
        # Calcul le projetté de la coordonné "x" selon la perspective et le recul de la caméra.
        # Notez que l'axe "z" est utilisé dans les deux calculs, au profit de "x" et "y".
        pX = math.floor( (point["x"] * perspective) / (point["z"] - cameraZ) + width/2 )
        pY = math.floor( (point["y"] * perspective) / (point["z"] - cameraZ) + width/2 )

        # Coordonnées du pixel dans le calque de superposition.
        zbi = (pY,pX)

        # Si le pixel n'a jamais été dessiné OU si c'est le cas…
        # … mais que sa coordonnée "z" est inférieur au pixel déjà dessiné
        # (et est donc plus proche de la caméra).
        if not zBuffer.has_key(zbi) or point["z"] < zBuffer[zbi]:
            # On garde en mémoire le pixel dessiné dans le calque de superposition.
            zBuffer[zbi] = point["z"]

            # Dessine le pixel dans l'image.
            fill = ( int(point["r"]), int(point["g"]), int(point["b"]) )
            draw.point( (int(pX),int(pY)), fill )



import random
# Nombres de points à dessiner
for i in range(90000):
    # Valeurs dans [0,1[
    a = random.random()
    b = random.random()

    # Rayons du cœur et des pétals
    r_heart = 25
    r_petal = 50

    # coeur
    draw_point( sphere( a, b, r_heart ) )
    # pétale du haut
    # Les valeurs des déplacements sont arbitraires et dépendent de ce que vous souhaitez faire.
    draw_point( move( petal( a,b, r_petal ), 0, -70, 0 ) )
    # De même pour les rotations.
    # pétale du bas
    draw_point( move( rotate_x( petal( a,b, r_petal ), 1.15*math.pi ), -2, 141, -10 ) )
    # pétale de gauche
    draw_point( move( rotate_z( rotate_x( petal( a,b, r_petal ), -0.3*math.pi ), math.pi/6 ), -50, 10, 25 ) )
    # pétale de droite
    draw_point( move( rotate_z( rotate_x( petal( a,b, r_petal ), -0.3*math.pi ), -math.pi/6 ), 60, 55, 25 ) )
    # tige
    draw_point( move( rotate_x( cylinder( a,b, r_heart/4, 400 ), math.pi/2 ), 55, 250, 250 ) )

# Écris l'image dans un fichier au format « Portable Network Graphics », compressé sans perte.
im.save("paquerette.png", "PNG")

