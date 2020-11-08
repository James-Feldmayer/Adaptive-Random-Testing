
class ART:
    def __init__(self, input_domain):
        self.S = self.theorem_1(input_domain)

        self.total_attempts = 0
        self.total_failures = 0

        self._running = False

    def distance(self, selected_case):  # equation 3
        total_distance = 0

        for i in range(0, len(self.S)):
            total_distance += (self.total_attempts -
                               self.S[i][selected_case[i]])

        return total_distance

    def theorem_1(self, input_domain):  # [1, 2] -> [[0], [0, 0]]
        tabulation_table = []

        for element in input_domain:
            tabulation_table.append([0] * element)  # [0] * 3 -> [0, 0, 0]

        return tabulation_table

    def update_s(self, selected_case):
        for i in range(0, len(self.S)):
            self.S[i][selected_case[i]] += 1

    def main(self):

        while self._running:

            best_candidate = []  # random case
            most_different = self.distance(best_candidate)

            k = 3  # number of candidates

            for e in range(0, k):
                candidate = []  # new case
                difference = self.distance(candidate)

                if (difference > most_different):  # should probably write a candidate class
                    best_candidate = candidate
                    most_different = difference

            try:
                global user_function  # change this to use our case
                user_function(usable_case(best_candidate))
            except:
                self.total_failures += 1

                print(usable_case(best_candidate))

            self.total_attempts += 1  # number of test cases
            self.update_s(best_candidate)


def start_function():
    if(True):
        global random_method
        random_method._running = True
        thread = Thread(target=random_method.main)
        thread.start()


def stop_function():
    global random_method
    random_method._running = False


random_method = ART([1, 2, 3])  # RT()

random_method.main()

# window.mainloop()
