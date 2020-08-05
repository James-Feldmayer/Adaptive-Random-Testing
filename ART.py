
from graphics import *

def draw_point(point):
    point.draw(window)

def random_point(width, height):
    import random
    return Point(random.randrange(0, width), random.randrange(0, height))

def euclidean_distance(first, second):
    import numpy
    a = numpy.array(first)
    b = numpy.array(second)
    print(numpy.linalg.norm(a-b))

def random_tesing(width, height):
    rt = []

    for i in range(10):
        rt.append(random_point(width, height))
        
    for t in rt:
        draw_point(t)

def adaptive_random_testing(width, height):
    art = []

    for i in range(10):
        art.append(random_point(width, height))
        
    print(art)

def draw_square_failure_region(length):

    point = random_point(400, 400)

    rectangle = Rectangle(Point(point.x, point.y), Point(point.x+length, point.y+length))
    rectangle.setFill("red")
    rectangle.setOutline("red")
    rectangle.draw(window)

width = 400
height = 400

"""
width = int(input("what is the width? "))
height = int(input("what is the height? "))
"""

failure_rate = float(input("What is the failure rate? "))
if failure_rate <= 0:
    raise Exception("The failure rate should be greater than 0")
if failure_rate >= 1:
    raise Exception("The failure rate should be less than 1") 

window = GraphWin(width = width, height = height)

draw_square_failure_region(int(width*failure_rate))

# euclidean_distance(random_point(0, 10), random_point(0, 10))

random_tesing(width, height)

# adaptive_random_testing(width, height)

#for i in range(1, 10):
#    print("Test case {}: RT - {};     ART - {}".format(i, "missed", "HIT!!!"))

import time
time.sleep(10)
