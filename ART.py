
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

def random_tesing(top_left, bottom_right, width, height, wait = False):
    while(True):
    
    #for i in range(0, 10):
     
        point = random_point(width, height)

        draw_point(point)

        if failure_detected(top_left, bottom_right, point):
            print("HIT!!!")
            break
        
        if wait:
            import time
            time.sleep(1)

def adaptive_random_testing(width, height):
    art = []

    for i in range(10):
        art.append(random_point(width, height))
        
    print(art)

def failure_region(length):

    point = random_point(400, 400)

    offset = Point(0, 0)

    if point.x+length > 400:
        offset.x = point.x+length-400
    if point.y+length > 400:
        offset.y = point.y+length-400

    top_left = Point(point.x-offset.x, point.y-offset.y)
    bottom_right = Point(point.x+length-offset.x, point.y+length-offset.y)

    return top_left, bottom_right

def draw_failure_region(top_left, bottom_right):
    rectangle = Rectangle(top_left, bottom_right)
    rectangle.setFill("red")
    rectangle.setOutline("red")
    rectangle.draw(window)

def write_some_text():
    txt = Text(Point(400, 250), "Hello and welcome to FizzBuzz!")
    txt.setSize(22)
    txt.setFace("courier")
    txt.draw(window)

def failure_detected(top_left, bottom_right, attempt, print = False):

    too_high = not attempt.y >= top_left.y
    too_low = not attempt.y <= bottom_right.y
    too_left = not attempt.x >= top_left.x
    too_right = not attempt.x <= bottom_right.x

    if print:
        if too_high:
            print("too high") 
        
        if too_low:
            print("too low")
        
        if too_left: 
            print("too left")
        
        if too_right:
            print("too right")
        
    return not too_high and not too_low and not too_left and not too_right

# just gonna put the whole thing inside a box
# and I will be well on my way

# probably not a good idea to have the whole thing 
# based on fitting inside the canvas anyway

# does the size of the input space need to be 
# variable?

width = 400
height = 400

# not sure if we need to be able to do this or not?
# probably not very difficult though

# width = int(input("What is the width? "))
# height = int(input("What is the height? "))

failure_rate = float(input("What is the failure rate? "))
if failure_rate <= 0:
    raise Exception("The failure rate should be greater than 0")
if failure_rate >= 1:
    raise Exception("The failure rate should be less than 1") 

window = GraphWin(width = width, height = height)

# top_left, bottom_right 
# width, heigh

# very ugly

# really need to figure this out

# top_left and bottom_right are the 
# courner points of the failure region 

top_left, bottom_right = failure_region(int(width*failure_rate))
draw_failure_region(top_left, bottom_right)
random_tesing(top_left, bottom_right, width, height)

window.getMouse()
