import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    normalize(normal)
    normalize(light[LOCATION])
    normalize(view)

    ia = calculate_ambient(ambient, areflect)
    id = calculate_diffuse(light, dreflect, normal)
    isp = calculate_specular(light, sreflect, view, normal)
    rgb = [
        int(ia[0] + id[0] + isp[0]),
        int(ia[1] + id[1] + isp[1]),
        int(ia[2] + id[2] + isp[2])
        ]

    return limit_color(rgb)

def calculate_ambient(alight, areflect):
    ambi = [alight[0]* areflect[0],
            alight[1]* areflect[1],
            alight[2]* areflect[2]
            ]
    return ambi

def calculate_diffuse(light, dreflect, normal):
    dp = dot_product(normal, light[LOCATION])
    diff = [
        light[COLOR][0] * dreflect[0] * dp,
        light[COLOR][1] * dreflect[1] * dp,
        light[COLOR][2] * dreflect[2] * dp
    ]
    return diff

def calculate_specular(light, sreflect, view, normal):
    cos = dot_product(normal, light[LOCATION])
    r = [ (2 * normal[0] * cos) - light[LOCATION][0],
          (2 * normal[1] * cos) - light[LOCATION][1],
          (2 * normal[2] * cos) - light[LOCATION][2]
    ]

    cosalpha = dot_product(r, view)
    if (cosalpha < 0):
        cosalpha = 0
    cosalpha ** SPECULAR_EXP
    spec = [
            light[COLOR][0] * sreflect[0] * (cosalpha ** SPECULAR_EXP),
            light[COLOR][1] * sreflect[1] * (cosalpha ** SPECULAR_EXP),
            light[COLOR][2] * sreflect[2] * (cosalpha ** SPECULAR_EXP)
        ]
    return spec

def limit_color(color):
    for i in range(3):
        if (color[i] > 255):
            color[i] = 255
        if (color[i] < 0):
            color[i] = 0
    return color
#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
