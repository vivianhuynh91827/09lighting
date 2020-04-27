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
    #normalizing vectors
    normalize(normal)
    normalize(light[LOCATION])
    normalize(view)

    Ia = calculate_ambient(ambient, areflect)
    Id = calculate_diffuse(light, dreflect, normal)
    Is = calculate_specular(light, sreflect, view, normal)

    I = []
    I.append(int(Ia[0] + Id[0] + Is[0]))
    I.append(int(Ia[1] + Id[1] + Is[1]))
    I.append(int(Ia[2] + Id[2] + Is[2]))

    return I

def calculate_ambient(alight, areflect):
    Ia = []
    Ia.append(alight[0] * areflect[0])
    Ia.append(alight[1] * areflect[1])
    Ia.append(alight[2] * areflect[2])
    limit_color(Ia)
    return Ia

def calculate_diffuse(light, dreflect, normal):
    x = dot_product(normal, light[0])
    if x < 0:
        x = 0

    Id = []
    Id.append(light[1][0] * dreflect[0] * x)
    Id.append(light[1][1] * dreflect[0] * x)
    Id.append(light[1][2] * dreflect[0] * x)
    limit_color(Id)
    return Id

def calculate_specular(light, sreflect, view, normal):
    x = dot_product(normal, light[0]) * 2
    #normal
    N = []
    N.append((x * normal[0]) - light[0][0])
    N.append((x * normal[1]) - light[0][1])
    N.append((x * normal[2]) - light[0][2])

    x = dot_product(N, view)
    if x < 0:
        x = 0
    x = pow(x, SPECULAR_EXP)
    Is = []
    Is.append(x * light[1][0] * sreflect[0])
    Is.append(x * light[1][1] * sreflect[1])
    Is.append(x * light[1][2] * sreflect[2])
    limit_color(Is)
    return Is


def limit_color(color):
    for i in range(3):
        color[i] = int(color[i])
        if color[i] > 255:
            color[i] = 255
        if color[i] < 0:
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
