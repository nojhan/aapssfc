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

def sphere(a, b, radius):
    """Prend des coordonnées 2D ("a" et "b") entre 0 et 1 et les déforment
    de manière à les placer dans un cercle de rayon "radius".
    Ajoute de la profondeur et un gradient de couleur jaune."""

    # Angle en radian (pi/2 = 180°)
    angle = a * math.pi * 2

    # Centre du cercle
    x0 = radius*2
    y0 = radius*2

    return {"x":math.cos(angle) * radius * b + x0, # projection de a vers x
            "y":math.sin(angle) * radius * b + y0 ,# projection de b vers y
            "z": b * radius - radius / 2,          # profondeur
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
    """

    angle = a * 2*math.pi

    return {"x": math.cos(angle) * radius,
            "y": math.sin(angle) * radius,
            "z": b * length - length / 2, # centrage du cylindre
            "r": 0,
            "g": math.floor(b*255),
            "b": 0 }

def rotate_x( d, a ):
    if d:
        d["y"] = d["y"] * math.cos(a) - d["z"] * math.sin(a)
        d["z"] = d["y"] * math.sin(a) + d["z"] * math.cos(a)
        return d
    else:
        return None


def rotate_y( d, a ):
    if d:
        d["z"] = d["z"] * math.cos(a) - d["x"] * math.sin(a)
        d["x"] = d["z"] * math.sin(a) + d["x"] * math.cos(a)
        return d
    else:
        return None


def rotate_z( d, a ):
    if d:
        d["x"] = d["x"] * math.cos(a) - d["y"] * math.sin(a)
        d["y"] = d["x"] * math.sin(a) + d["y"] * math.cos(a)
        return d
    else:
        return None


def move( d, dx, dy, dz ):
    if d:
        d["x"] = d["x"] + dx
        d["y"] = d["y"] + dy
        d["z"] = d["z"] + dz
        return d
    else:
        return None


def draw_point( point ):
    if point:
        pX = math.floor( (point["x"] * perspective) / (point["z"] - cameraZ) + width/2 )
        pY = math.floor( (point["y"] * perspective) / (point["z"] - cameraZ) + width/2 )
        zbi = pY * width + pX
        if not zBuffer.has_key(zbi) or point["z"] < zBuffer[zbi]:
            zBuffer[zbi] = point["z"]
            fill = ( int(point["r"]), int(point["g"]), int(point["b"]) )
            #fill = ( 10+int(zBuffer[zbi]), ) * 3
            draw.point( (int(pX),int(pY)), fill )



import random
# Nombres de points à dessiner
for i in range(90000):
    a = random.random()
    b = random.random()
    #     z
    #    /
    #   +-- x
    #   |
    #   y
    r_heart = 25
    r_petal = 50
    # coeur
    draw_point( sphere( a, b, r_heart ) )
    # pétale du haut
    draw_point( move( petal( a,b, r_petal ), 0, -70, 0 ) )
    # pétale du bas
    draw_point( move( rotate_x( petal( a,b, r_petal ), 1.15*math.pi ), -2, 141, -10 ) )
    # pétale de gauche
    draw_point( move( rotate_z( rotate_x( petal( a,b, r_petal ), -0.3*math.pi ), math.pi/6 ), -50, 10, 25 ) )
    # pétale de droite
    draw_point( move( rotate_z( rotate_x( petal( a,b, r_petal ), -0.3*math.pi ), -math.pi/6 ), 60, 55, 25 ) )
    # tige
    draw_point( move( rotate_x( cylinder( a,b, r_heart/4, 400 ), math.pi/2 ), 55, 250, 250 ) )

im.save("paquerette.png", "PNG")

