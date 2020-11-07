 
class ART:
    def __init__(self):
        self.A = []  # user input
        self.S = []  # calculate distance
        self.attempt = 0  # number of test cases
        self.failure = 0

        self._running = False

    def distance(self, candidate):  # equation 3
        accumulate = 0

        for i in range(0, self.g()):
            accumulate += (self.attempt - self.S[i][candidate[i]])

        return accumulate

    def theorem_1(self):
        S = []

        for domain in self.A:
            S.append(self.zeros(domain))

        return S

    def updateS(self, candidate):
        for i in range(0, self.g()):
            self.S[i][candidate[i]] += 1

    def main(self):

        while self._running:

            best_candidate = self.numeric_case()
            most_different = self.distance(best_candidate)

            k = 3  # number of candidates

            for k in range(0, k):
                candidate = self.numeric_case()
                difference = self.distance(candidate)

                if (difference > most_different):
                    best_candidate = candidate
                    most_different = difference

            try:
                global user_function
                user_function(usable_case(best_candidate))
            except:
                self.failure += 1

                # perhaps create a list of failure objects

                # print(usable_case(best_candidate))
                # attempt and display the number of failures

            self.attempt += 1  # number of test cases
            self.updateS(best_candidate)

            ###

            self.updateGUI()  # could probably use a better name


def startButton():
    if(True):

        global c
        c._running = True

        thread = Thread(target=c.main)
        thread.start()

        # need to add comments


def stopButton():
    global c
    c._running = False


random_method = ART()

window.mainloop()
