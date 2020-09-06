
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


def random_point(top_left, bottom_right, colour="black"):
    import random

    point = Point(random.randrange(int(top_left.x), int(bottom_right.x)),
                  random.randrange(int(top_left.y), int(bottom_right.y)))
    point.setFill(colour)
    point.setOutline(colour)

    return point


class Canvas:
    # a canvas represents the 2d input space of a program

    def __init__(self, top_left, bottom_right, failure_rate=0.01, regions=1):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.height = (self.bottom_right.y - self.top_left.y)
        self.width = (self.bottom_right.x - self.top_left.x)

        self.regions = regions
        self.region_width = self.width/self.regions
        self.region_height = self.height/self.regions

        self.failure_region = self.SquareFailureRegion(failure_rate)
        self.first_point = self.random_point(draw=False)

        # draw_solid_rectangle(top_left, bottom_right, "lime")

    def checkerboard(self):
        for x in range(0, self.regions):
            for y in range(0, self.regions):

                if ((y + (x % 2)) % 2) == 0:

                    draw_solid_rectangle(
                        Point(x*self.region_width+self.top_left.x, y*self.region_height+self.top_left.y), Point(x*self.region_width+self.region_width+self.top_left.x, y*self.region_height+self.region_height+self.top_left.y), "yellow")

    def random_point(self, draw=False, colour="black"):
        point = random_point(self.top_left, self.bottom_right, colour)

        if draw:
            point.setFill(colour)
            point.setFill(colour)
            point.draw(window)

        return point

    # must not display an object twice
    # issue with displaying a duplicate object?

    def display(self, checkerboard=False, colour="lime"):
        draw_solid_rectangle(self.top_left, self.bottom_right, colour)

        if checkerboard:
            self.checkerboard()

        self.failure_region.display()
        self.first_point.draw(window)

    def SquareFailureRegion(self, failure_rate):

        failure_height = self.height*failure_rate
        failure_width = self.width*failure_rate

        safe_point = random_point(self.top_left, Point(
            self.top_left.x+self.width-failure_width, self.top_left.y+self.height-failure_height))

        return FailureRegion(safe_point, Point(
            safe_point.x+failure_width, safe_point.y+failure_height))

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

    def sum_dist(self, count, candidate, S):  # equation 3

        output = (count - S[0][int((candidate[0] -
                                    self.top_left.x) / self.region_width)])

        output += (count - S[1][int((candidate[1] -
                                     self.top_left.y) / self.region_width)])

        return output

    def theorem_1(self, h=[10, 10]):

        g = len(h)

        S = []

        for category in range(0, g):

            choices = []

            for choice in range(0, h[category]):
                choices.append(0)

            S.append(choices)

        return S

    def ARTsum(self, draw=True, wait=False):
        S = self.theorem_1(h=[self.regions, self.regions])

        count = 1  # number of test cases

        most_different = 0
        best_candidate = self.first_point

        # I think it is working now
        # but still seems a little buggy
        # compare to random testing

        while(True):

            sleep(wait)

            if self.failure_region.failure_detected(best_candidate):
                return count

            S[0][int((best_candidate.x-self.top_left.x) / self.region_width)] += 1
            S[1][int((best_candidate.y-self.top_left.y) / self.region_height)] += 1

            k = 10  # number of candidates

            candidates = []  # , draw=True

            for k in range(0, k):
                candidates.append(self.random_point(colour="red"))

            for candidate in candidates:

                difference = self.sum_dist(
                    count, [int(candidate.x), int(candidate.y)], S)

                # larger is more different

                if (difference > most_different):
                    best_candidate = candidate
                    most_different = difference

            # window.getMouse()

            most_different = 0

            for candidate in candidates:
                candidate.undraw()

            if draw:
                best_candidate.setFill("black")
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


# is there any research to say how we should pick the regions?
# (to catagorize a numeric field)
# maybe do my own experiments?


runs = 100  # int(input("How many tests would you like to run? "))
print()

rt_total_attempts = 0
art_total_attempts = 0
rt_wins = 0
art_wins = 0
draws = 0

for i in range(0, runs):
    rt_canvas = Canvas(Point(50, 50), Point(400, 400), 0.01, regions=10)
    art_canvas = copy.deepcopy(rt_canvas)
    art_canvas.translate(450, 0)

    rt_attempts = rt_canvas.RT(draw=False)
    art_attempts = art_canvas.ARTsum(draw=False)

    rt_total_attempts += rt_attempts
    art_total_attempts += art_attempts

    if art_attempts < rt_attempts:
        art_wins += 1
    elif rt_attempts < art_attempts:
        rt_wins += 1
    else:
        draws += 1

print("rt wins: {}".format(rt_wins))
print("rt total guesses: {}".format(rt_total_attempts))
print()
print("art-sum wins: {}".format(art_wins))
print("art-sum total guesses: {}".format(art_total_attempts))
print()
print("draws: {}".format(draws))

# f-measure is not significantly
# fscs-art has f-measure 0.5

# art-sum has f-measure 0.73
