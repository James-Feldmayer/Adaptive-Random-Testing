
# somewhat generic implementation

h = [30, 2, 100]  # user input
g = len(h)


# numeric to non-numeric
def usable_case(numeric_list):  # user input

    non_numeric = []

    #

    return non_numeric

# need to use this function to test


def zeros(length):
    vector = []

    for i in range(0, length):
        vector.append(0)

    return vector


def numeric_case(h=h):
    import random

    numeric_list = []

    for domain in h:
        numeric_list.append(random.randrange(0, domain))

    return numeric_list


def distance(test_cases, candidate, S):  # equation 3
    accumulate = 0

    for i in range(0, g):
        accumulate += (test_cases - S[i][candidate[i]])

    return accumulate


def theorem_1(h=h):
    S = []

    for domain in h:
        S.append(zeros(domain))

    return S


def updateS(candidate, S):
    for i in range(0, g):
        S[i][candidate[i]] += 1

# bad exit condidtion
# should wait to be interupted

# going to use "usable_case" to transform

# automatically generated numeric test case
# into a usable non-numeric test case


def ARTsum():
    S = theorem_1()
    best_candidate = numeric_case()
    test_cases = 0

    while(True):
        most_different = 0  # s
        test_cases += 1  # number of test cases

        if (test_cases == 100):
            return test_cases

        # update S
        for i in range(0, g):
            S[i][best_candidate[i]] += 1

        k = 3  # number of candidates

        for k in range(0, k):
            candidate = numeric_case()

            difference = distance(test_cases, candidate, S)

            if (difference > most_different):
                best_candidate = candidate
                most_different = difference


ARTsum()

# metamorphic relations
# fuzzing

# define categories and choices for non-numerics
# ranges and precision for numerics
