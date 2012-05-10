#encoding: utf-8

import math

import Image
import ImageDraw
import ImageColor

width = 500
perspective = width
cameraZ = -width
zBuffer = {}

im = Image.new("RGB", (width,width) )
draw = ImageDraw.Draw(im)


def sphere(a, b, radius):
    angle = a * math.pi * 2
    x0 = radius*2
    y0 = radius*2

    return {"x":math.cos(angle) * radius * b + x0,
            "y":math.sin(angle) * radius * b + y0 ,
            "z": b * radius - radius / 2, 
            "r": 50 + math.floor((1 - b**2) * 300),
            "g": 50 + math.floor((1 - b**2) * 200),
            "b": 0,
            }


def petal(a,b,radius):
    x = a * radius*2
    y = b * radius*2
    x0 = radius
    y0 = radius

    # Note : prendre les racines carrées ne fait que rajouter une opération coûteuse inutile
    if (x - x0) * (x - x0) + (y - y0) * (y - y0) < radius * radius:
        return {"x": x,
                "y": y * (1 + b) / 2,
                "z": b * radius - radius / 2, 
                "r": 100 + math.floor((1 - b) * 155),
                "g": 100 + math.floor((1 - b) * 155),
                "b": 100 + math.floor((1 - b) * 155)
                }
    else:
        return None


def cylinder( a,b, radius=100, length=400 ):
    angle = a * 2*math.pi

    return {"x": math.cos(angle) * radius,
            "y": math.sin(angle) * radius,
            "z": b * length - length / 2, 
            "r": 0,
            "g": math.floor(b*255),
            "b": 0 }


def if_none( func ):
    """Ce décorateur permet de rajouter un test « autour » d'une fonction passée en argument.
    Ici, il s'agit de n'appliquer la fonction décorée que si le premier argument est défini."""

    # Le nom de la fonction embarquée importe peu.
    def wrapper( *args, **kwargs ):
        """Si le premier argument n'est pas "None", applique la fonction, sinon, le renvoie."""
        if args[0]:
            return func( *args, **kwargs )
        else:
            return None
    return wrapper


# Le décorateur est appelé en premier lors de l'appel aux fonctions,
# ce qui détermine si la fonction est réellement appelé (si le premier argument existe)
# ou non (si l'argument n'existe pas).
@if_none
def rotate_x( d, a ):
    d["y"] = d["y"] * math.cos(a) - d["z"] * math.sin(a)
    d["z"] = d["y"] * math.sin(a) + d["z"] * math.cos(a)
    return d


@if_none
def rotate_y( d, a ):
    d["z"] = d["z"] * math.cos(a) - d["x"] * math.sin(a)
    d["x"] = d["z"] * math.sin(a) + d["x"] * math.cos(a)
    return d


@if_none
def rotate_z( d, a ):
    d["x"] = d["x"] * math.cos(a) - d["y"] * math.sin(a)
    d["y"] = d["x"] * math.sin(a) + d["y"] * math.cos(a)
    return d


@if_none
def move( d, dx, dy, dz ):
    d["x"] = d["x"] + dx
    d["y"] = d["y"] + dy
    d["z"] = d["z"] + dz
    return d


def draw_point( point ):
    if point:
        pX = math.floor( (point["x"] * perspective) / (point["z"] - cameraZ) + width/2 )
        pY = math.floor( (point["y"] * perspective) / (point["z"] - cameraZ) + width/2 )
        zbi = pY * width + pX
        if not zBuffer.has_key(zbi) or point["z"] < zBuffer[zbi]:
            zBuffer[zbi] = point["z"]
            fill = ( int(point["r"]), int(point["g"]), int(point["b"]) )
            # On pourrait ne dessiner que la profondeur des objets 
            # en n'utilisant qu'un gradient de blanc calculé sur "z" :
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

