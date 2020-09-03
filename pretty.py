
from graphics import *
import copy


def euclidean_distance(pointA, pointB):
    import numpy
    a = numpy.array([pointA.x, pointA.y])
    b = numpy.array([pointB.x, pointB.y])
    return numpy.linalg.norm(a-b)


def manhattan_distance(pointA, pointB):
    return abs(pointA.x - pointB.x) + abs(pointA.y - pointB.y)


def chebyshev_distance(pointA, pointB):
    return max(abs(pointA.x - pointB.x), abs(pointA.y - pointB.y))


def calculate_minimum_distance(test_cases, new_point):
    minimum_distance = euclidean_distance(test_cases[0], new_point)

    for i in range(1, len(test_cases)):
        new_distance = euclidean_distance(test_cases[i], new_point)
        if new_distance < minimum_distance:
            minimum_distance = new_distance

    return minimum_distance


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
        self.first_point = self.random_point(draw=False)

    def random_point(self, draw=False):
        point = random_point(self.top_left, self.bottom_right)

        if draw:
            point.draw(window)

        return point

    def display(self, colour="lime"):
        draw_solid_rectangle(self.top_left, self.bottom_right, colour)
        self.failure_region.display()

        # this line causes an error if called before deep.deepcopy
        self.first_point.draw(window)

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
        self.first_point.x += horiztonal
        self.first_point.y += vertical

        self.failure_region.translate(horiztonal, vertical)

    def FSCS_ART(self, rt_score=0, draw=True, wait=False):

        count = 1

        if self.failure_region.failure_detected(self.first_point):
            return count

        test_cases = [self.first_point]

        while(True):

            sleep(wait)

            count += 1

            # refactor this as its own function

            largest_minimum_distance_point = Point(0, 10)

            largest_minimum_distance = 0
            for i in range(0, 10):
                new_point = self.random_point(draw=False)

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

            if rt_score > 0 & count > rt_score:
                return count

            test_cases.append(largest_minimum_distance_point)

    # make as many methods free as possible

    def sum_dist(self, n, candidate, S):  # equation 3

        output = 0

        for i in range(0, len(S)):  # category
            output += (n - S[i][int(candidate[i] / 30)])

        return output

    def theorem_1(self, g=2, h=[10, 10]):

        categories = []

        for category in range(0, g):

            choices = []

            for choice in range(0, h[category]):
                choices.append(0)

            categories.append(choices)

        return categories

# does not seem to do anything

    def ARTsum(self, draw=True, wait=False):
        S = self.theorem_1()  # theorem 1

        count = 1  # number of test cases

        most_different = 0
        best_candidate = self.first_point

        while(True):

            sleep(wait)

            if self.failure_region.failure_detected(best_candidate):
                return count

            S[0][int(best_candidate.x / 30)] += 1
            S[1][int(best_candidate.y / 30)] += 1

            for i in range(0, k := 3):  # number of candidates

                candidate = self.random_point()
                difference = self.sum_dist(
                    count, [int(candidate.x), int(candidate.y)], S)

                if (difference > most_different):
                    best_candidate = candidate

            if draw:
                best_candidate.draw(window)

            count += 1

    def RT(self, draw=True, wait=False):

        count = 1
        point = self.first_point

        while (True):

            sleep(wait)

            if self.failure_region.failure_detected(point):
                return count

            count += 1
            point = self.random_point(draw)


def sleep(wait=True, second=1):
    if wait:
        time.sleep(second)


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


class Scoreboard:

    first_wins = 0
    second_wins = 0
    draws = 0

    def __init__(self, second_algorithm):
        self.first_algorithm = "rt"
        self.second_algorithm = second_algorithm

    def race(self, first_score, second_score):
        if first_score < second_score:
            self.first_wins += 1

        elif second_score < first_score:
            self.second_wins += 1

        elif first_score == second_score:
            self.draws += 1

    def display(self):
        print("{} wins: {}".format(self.first_algorithm, self.first_wins))
        print("{} wins: {}".format(self.second_algorithm, self.second_wins))
        print("draws: {}".format(self.draws))


window = GraphWin(width=900, height=450)

rt_canvas = Canvas(Point(50, 50), Point(400, 400), 0.05)
art_canvas = copy.deepcopy(rt_canvas)
art_canvas.translate(450, 0)

rt_canvas.display()
art_canvas.display()

header1 = Text(Point(75, 20), 'RT')
header1.draw(window)

header2 = Text(Point(550, 20), 'ARTsum')
header2.draw(window)

rt_score = rt_canvas.RT()
art_score = art_canvas.ARTsum()

score1 = Text(Point(125, 20), rt_score)
score1.draw(window)

art_score = 0

score2 = Text(Point(600, 20), art_score)
score2.draw(window)

window.getMouse()
