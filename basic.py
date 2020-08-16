
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
    return Point(random.randrange(int(top_left.x), int(bottom_right.x)), random.randrange(int(top_left.y), int(bottom_right.y)))


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

    # still does not work as intended
    # it is not balanced
    # it does pointy rectangles and then it flips
    # this is particularly noticable when
    # you use a smaller error rate

    # smaller error rate -> much pointier
    # remember the average should be

    # the flipping is an code smell
    # its just a bandaid for bad code

    # should use these limits but not
    # generate based on them

    #

    # need to get the math
    # not sure how to prove what the issue is

    def RectangleFailureRegion(self, failure_rate):

        canvas_width = (self.bottom_right.x - self.top_left.x)
        canvas_height = (self.bottom_right.y - self.top_left.y)
        canvas_area = canvas_width*canvas_height
        failure_area = canvas_area*failure_rate

        import random

        rectangle_width = 0
        rectangle_height = 0

        print((canvas_width * 0.9+canvas_width)/2)
        # as the error rate decreases
        # the range widens
        # random.randrange(canvas_width * failure_rate, canvas_width)
        #
        # 75% of the time is horizontal
        # as the error rate changes

        if(random.randrange(0, 2)):
            rectangle_width = random.randrange(
                canvas_width * failure_rate, canvas_width)
            rectangle_height = failure_area / rectangle_width

        else:
            rectangle_height = random.randrange(
                canvas_width * failure_rate, canvas_width)
            rectangle_width = failure_area / rectangle_height

        draw_solid_rectangle(self.top_left, Point(
            canvas_width-(self.top_left.x+rectangle_width), canvas_height-(self.top_left.y+rectangle_height)), "blue")

        point = random_point(self.top_left, Point(
            canvas_width-(self.top_left.x+rectangle_width), canvas_height-(self.top_left.y+rectangle_height)))

        return FailureRegion(point, Point(point.x+rectangle_width, point.y+rectangle_height))

    def SquareFailureRegion(self, failure_rate):

        canvas_height = (self.bottom_right.y - self.top_left.y)
        canvas_width = (self.bottom_right.x - self.top_left.x)

        draw_solid_rectangle(self.top_left, Point(
            self.top_left.x+canvas_width*(1 - failure_rate), self.top_left.y+canvas_height*(1 - failure_rate)), "blue")

        point = random_point(self.top_left, Point(
            self.top_left.x+canvas_width*(1 - failure_rate), self.top_left.y+canvas_height*(1 - failure_rate)))

        return FailureRegion(point, Point(point.x+canvas_width*failure_rate, point.y+canvas_height*failure_rate))


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


"""
width = int(input("What is the width? "))
height = int(input("What is the height? "))
"""

# window = GraphWin(width=800, height=800)
window = GraphWin(width=400, height=400)

"""
failure_rate = float(input("What is the failure rate? "))
# failure_rate = 0.3

if failure_rate <= 0:
    raise Exception("The failure rate should be greater than 0")
if failure_rate >= 1:
    raise Exception("The failure rate should be less than 1")
"""

# canvas = Canvas(Point(100, 100), Point(500, 500))
canvas = Canvas(Point(0, 0), Point(400, 400))

failure_region = canvas.RectangleFailureRegion(0.01)

for i in range(0, 10):
    canvas.draw_random_point()

window.getMouse()
