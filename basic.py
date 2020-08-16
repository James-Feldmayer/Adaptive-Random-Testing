
from graphics import *


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
    return Point(random.randrange(top_left.x, bottom_right.x), random.randrange(top_left.y, bottom_right.y))


class Canvas:
    # a canvas represents the 2d input space of a program

    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.draw_solid_rectangle("lime")

    def random_point(self):
        return random_point(self.top_left, self.bottom_right)

    def draw_random_point(self):
        self.random_point().draw(window)

    """
    def test_point(self, attempt):
        attempt.draw(window)
        return self.failure_detected(attempt)
    """

    def draw_solid_rectangle(self, colour):
        draw_solid_rectangle(self.top_left, self.bottom_right, colour)

    def FSCS_ART(self):
        test_cases = []

        first_point = self.random_point()

        if self.test_point(first_point):
            # print("HIT!!!")
            return 1

        test_cases.append(first_point)

        count = 1

        while(True):

            count += 1

            # refactor this as its own function

            largest_minimum_distance_point = Point(0, 0)

            largest_minimum_distance = 0
            for i in range(0, k := 10):
                new_point = self.random_point()
                new_minimum_distance = calculate_minimum_distance(
                    test_cases, new_point)
                if new_minimum_distance > largest_minimum_distance:
                    largest_minimum_distance = new_minimum_distance
                    largest_minimum_distance_point = new_point

            # test the program using t as a test case
            # using "largest_minimum_distance_point"

            if test_point(largest_minimum_distance_point):
                # print("HIT!!!")
                return count

            test_cases.append(largest_minimum_distance_point)

    def RT(self, wait=False):

        count = 0

        while(True):
            count += 1

            if test_point(self.random_point()):
                # print("HIT!!!")
                return count

            if wait:
                import time
                time.sleep(1)

    def RectangleFailureRegion(self, failure_rate):

        square_width = (self.bottom_right.x - self.top_left.x)
        square_height = (self.bottom_right.y - self.top_left.y)
        square_area = square_width*square_height
        failure_area = square_area*failure_rate

        import random

        # dosn't work real well
        # gives correct test cases but very uneven distribution

        rectangle_width = int(square_width * failure_rate *
                              random.randrange(1, pow(failure_rate, -1)))

        # 1-2 vertical
        # 3 square
        # 4-10 horizontal

        # horizontal 70% of the time
        # need to fix this

        # could swap focus
        # use rectangle_width vs rectangle_height as the random one
        # should even it out quite a bit
        # but is still a mediocre solution

        rectangle_height = int(failure_area / rectangle_width)

        draw_solid_rectangle(Point(self.top_left.x, self.top_left.y), Point(
            self.top_left.x+rectangle_width, self.top_left.y+rectangle_height), "blue")

        # point = random_point(Point(self.top_left.x, self.top_left.y), Point(
        # self.top_left.x+square_width*(1 - failure_rate), self.top_left.y+square_height*(1 - failure_rate)))

        # return FailureRegion(point, Point(point.x+square_width*failure_rate, point.y+square_height*failure_rate))

    def SquareFailureRegion(self, failure_rate):

        square_height = (self.bottom_right.y - self.top_left.y)
        square_width = (self.bottom_right.x - self.top_left.x)

        draw_solid_rectangle(Point(self.top_left.x, self.top_left.y), Point(
            self.top_left.x+square_width*(1 - failure_rate), self.top_left.y+square_height*(1 - failure_rate)), "blue")

        point = random_point(Point(self.top_left.x, self.top_left.y), Point(
            self.top_left.x+square_width*(1 - failure_rate), self.top_left.y+square_height*(1 - failure_rate)))

        return FailureRegion(point, Point(point.x+square_width*failure_rate, point.y+square_height*failure_rate))

# need to write a function which creates a
# FailureRegion from a Canvas
# square_ basically already exists
# needs a better name


class FailureRegion(Canvas):

    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.draw_solid_rectangle("red")

    def failure_detected(self, attempt):
        too_high = not attempt.y >= self.top_left.y
        too_low = not attempt.y <= self.bottom_right.y
        too_left = not attempt.x >= self.top_left.x
        too_right = not attempt.x <= self.bottom_right.x

        if False:
            if too_high:
                print("too high")

            if too_low:
                print("too low")

            if too_left:
                print("too left")

            if too_right:
                print("too right")

        return not too_high and not too_low and not too_left and not too_right


"""
width = int(input("What is the width? "))
height = int(input("What is the height? "))
"""

window = GraphWin(width=800, height=800)

"""
failure_rate = float(input("What is the failure rate? "))
# failure_rate = 0.3

if failure_rate <= 0:
    raise Exception("The failure rate should be greater than 0")
if failure_rate >= 1:
    raise Exception("The failure rate should be less than 1")
"""

canvas = Canvas(Point(100, 100), Point(500, 500))

failure_region = canvas.RectangleFailureRegion(0.1)

for i in range(0, 10):
    canvas.draw_random_point()

window.getMouse()
