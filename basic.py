
import copy
from graphics import *


# surely there is some speed advantage here

def euclidean_distance(pointA, pointB):
    import numpy
    a = numpy.array([pointA.x, pointA.y])
    b = numpy.array([pointB.x, pointB.y])
    return numpy.linalg.norm(a-b)


def calculate_minimum_distance(test_cases, new_point):
    distances = []

    for point in test_cases:
        distances.append(euclidean_distance(point, new_point))

    return min(distances)


#

def draw_solid_rectangle(top_left, bottom_right, colour):
    rectangle = Rectangle(top_left, bottom_right)
    rectangle.setFill(colour)
    rectangle.setOutline(colour)
    rectangle.draw(window)


def random_point(top_left, bottom_right):
    import random
    return Point(random.randrange(int(top_left.x), int(bottom_right.x)), random.randrange(int(top_left.y), int(bottom_right.y)))


class Canvas:
    # a canvas represents the 2d input space of a program

    def __init__(self, top_left, bottom_right, failure_rate=0.01):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.failure_region = self.SquareFailureRegion(failure_rate)
        # self.display()

    def random_point(self):
        return random_point(self.top_left, self.bottom_right)

    def draw_random_point(self):
        self.random_point().draw(window)

    def display(self, colour="lime"):
        draw_solid_rectangle(self.top_left, self.bottom_right, colour)
        # print("print")
        self.failure_region.display()

    def SquareFailureRegion(self, failure_rate):
        canvas_height = (self.bottom_right.y - self.top_left.y)
        canvas_width = (self.bottom_right.x - self.top_left.x)

        safe_point = random_point(self.top_left, Point(
            self.top_left.x+canvas_width*(1 - failure_rate), self.top_left.y+canvas_height*(1 - failure_rate)))

        return FailureRegion(safe_point, Point(
            safe_point.x+canvas_width*failure_rate, safe_point.y+canvas_height*failure_rate))

    def translate(self, horiztonal, vertical):
        self.top_left.x += horiztonal
        self.top_left.y += vertical
        self.bottom_right.x += horiztonal
        self.bottom_right.y += vertical

        self.failure_region.translate(horiztonal, vertical)

    def FSCS_ART(self, draw=True):

        test_cases = []

        first_point = self.random_point()

        if draw:
            first_point.draw(window)

        if self.failure_region.failure_detected(first_point):
            # print("HIT!!!")
            return 1

        test_cases.append(first_point)

        count = 1

        while(True):

            # import time
            # time.sleep(1)

            count += 1

            # refactor this as its own function

            largest_minimum_distance_point = Point(0, 10)

            largest_minimum_distance = 0
            for i in range(0, 10):
                new_point = self.random_point()

                new_minimum_distance = calculate_minimum_distance(
                    test_cases, new_point)
                if new_minimum_distance > largest_minimum_distance:
                    largest_minimum_distance = new_minimum_distance
                    largest_minimum_distance_point = new_point

            # test the program using t as a test case
            # using "largest_minimum_distance_point"

            if draw:
                largest_minimum_distance_point.draw(window)

            if self.failure_region.failure_detected(largest_minimum_distance_point):
                # print("HIT!!!")
                return count

            test_cases.append(largest_minimum_distance_point)

            # time.sleep(1)

    def RT(self, draw=True, wait=False):

        count = 0

        while(True):
            count += 1

            point = self.random_point()

            if draw:
                point.draw(window)

            if self.failure_region.failure_detected(point):
                # print("HIT!!!")
                return count

            if wait:
                import time
                time.sleep(1)


class FailureRegion:

    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right

    def display(self, colour="red"):
        draw_solid_rectangle(self.top_left, self.bottom_right, "red")
        # print("print")

    def translate(self, horiztonal, vertical):
        self.top_left.x += horiztonal
        self.top_left.y += vertical
        self.bottom_right.x += horiztonal
        self.bottom_right.y += vertical

    def failure_detected(self, attempt):
        too_high = not attempt.y >= self.top_left.y
        too_low = not attempt.y <= self.bottom_right.y
        too_left = not attempt.x >= self.top_left.x
        too_right = not attempt.x <= self.bottom_right.x

        return not too_high and not too_low and not too_left and not too_right

# scoreboard
rt_total = 0
art_total = 0
rt_score = 0
art_score = 0
draw = 0

failure_rate = float(input("Enter failure rate: ")) # try 0.05
print()

window = GraphWin(width=1000, height=1000)

# default 0.01
rt_canvas = Canvas(Point(50, 50), Point(350, 350), failure_rate)
rt_canvas.display()

#

label2 = Text(Point(450, 20), 'FSCS-ART')
label2.draw(window)

label3 = Text(Point(100, 20), 'RT')
label3.draw(window)

#

art_canvas = copy.deepcopy(rt_canvas)
art_canvas.translate(350, 0)
art_canvas.display()

rt_count = rt_canvas.RT()
art_count = art_canvas.FSCS_ART()

#

winner = "an error occured"
if art_count < rt_count:
    winner = "FSCS-ART wins!"
elif art_count == rt_count:
    winner = "draw"
else:
    winner = "RT wins!"

#

label4 = Text(Point(400, 450), winner)
label4.draw(window)

label = Text(Point(150, 400), 'click the screen to close the window')
label.draw(window)

label1 = Text(Point(150, 450), 'then look at the terminal')
label1.draw(window)

#

window.getMouse()
window.close()

runs = int(input("How many tests would you like to run? "))

for i in range(0, runs):

    # default 0.01
    rt_canvas = Canvas(Point(50, 50), Point(350, 350), 0.1)

    art_canvas = copy.deepcopy(rt_canvas)
    art_canvas.translate(350, 0)

    rt_count = rt_canvas.RT(draw=False)
    art_count = art_canvas.FSCS_ART(draw=False)

    # tally
    art_total += art_count
    rt_total += rt_count

    if art_count < rt_count:
        art_score += 1

    elif rt_count < art_count:
        rt_score += 1

    else:
        draw += 1

    #print
    print("{} / {}".format(i+1, runs))

print()

print("rt wins: {}".format(rt_score))  # O (n)
print("rt total guesses: {}".format(rt_total))
print()
print("fscs-art wins: {}".format(art_score))  # O(n*n) very inefficient
print("fscs-art total guesses: {}".format(art_total))
print()
print("draws: {}".format(draw))

print()
