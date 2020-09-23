import tkinter as tk
from threading import Thread
import time
import re
import traceback
import ast

user_function = None

def transform(user_input_f):
    if type(re.match("def usable_case\(\S*\):", user_input_f)) == re.Match:
        # regex matched

        try:
            exec(user_input_f, globals())  # create usable_case(list)

            try:
                usable_case([7, 7, 6, 3, 13, 1, 22, 18, 17])
                return True
            except:
                print("An exception occurred")

        except:
            print("Failed to compile")
            # gui = traceback.format_exc()  # update the GUI
            traceback.print_exc()

    else:
        print("Did not contain function usable_case(list)")


class valid_program:
    def __init__(self):  # what if file does not exist?
        None

    def compile(self, code_location):
        try:
            user_code = self.code_string(code_location)
            exec(user_code, globals())
            return True

        except:
            print(f"Unable to compile program under test '{code_location}'")
            return False

    def code_string(self, code_location):
        accumulate = ""

        # use regex to ensure file is .py

        try:
            with open(code_location) as file:
                for line in file:
                    accumulate += line + '\n'
        except:
            print(f"Unable to open '{code_location}'")

        return accumulate

    def valid_function(self, function_name, valid_input):
        try:
            user_function = self.find_function(function_name)
            user_function(valid_input)
            return user_function

        except:
            print(f"User function fails expected case '{valid_input}'")

    def find_function(self, function_name):
        try:
            user_function = eval(function_name)
            return user_function
        except:
            print(f"Unable to find function '{function_name}'")


class Stopwatch:
    def __init__(self):
        self.total = 0
        self.end_time = 0
        self.start_time = 0
        self.running = False

    def time_lapsed(self):
        if self.running:
            self.end_time = time.time()
            self.total += (self.end_time - self.start_time)
            self.start_time = time.time()
        else:
            self.total += (self.end_time - self.start_time)
            self.start_time = time.time()
            self.end_time = time.time()

        return int(self.total)

    def start(self):
        if self.running == False:
            self.start_time = time.time()

        self.running = True

    def stop(self):
        if self.running:
            self.end_time = time.time()

        self.running = False


class CountdownTask:
    def __init__(self):
        self._running = False
        self._alive = True
        #
        self.s = Stopwatch()
        self.count = 0
        self.art = ART()

    def start(self):
        self._running = True
        self.s.start()

    def stop(self):
        self._running = False
        self.s.stop()

    def terminate(self):
        self._alive = False

    def updateGUI(self):
        if self.count > 0:
            NTText.set(self.count)
            RTText.set(self.rate())
            NFText.set(0)  # self.failures?

    def run(self):
        time.sleep(1)

        while self._alive:
            if self._running:
                print("n")

                self.count += 1

    def rate(self):
        # if self.s.time_lapsed() == 0:
        # return 0

        return int(self.count / (self.s.time_lapsed() + 0.1))

class Metronome:
    def __init__(self, c):
        self.c = c  # CountdownTask()
        self._alive = True

    def terminate(self):
        self._alive = False
        self.c.terminate()

    def run(self):
        time.sleep(1)
        while self._alive:
            self.c.updateGUI()
            time.sleep(0.1)

class ART:
    def __init__(self):
        self.h = []
        self.g = len(self.h)
        self._running = False

    def setH(self, h):
        self.h = h

    def zeros(self, length):
        vector = []

        for i in range(0, length):
            vector.append(0)

        return vector

    def numeric_case(self):
        import random

        numeric_list = []

        for domain in self.h:
            numeric_list.append(random.randrange(0, domain))

        return numeric_list

    def distance(self, test_cases, candidate, S):  # equation 3
        accumulate = 0

        for i in range(0, self.g):
            accumulate += (test_cases - S[i][candidate[i]])

        return accumulate

    def theorem_1(self):
        S = []

        for domain in self.h:
            S.append(self.zeros(domain))

        return S

    def updateS(self, candidate, S):
        for i in range(0, self.g):
            S[i][candidate[i]] += 1

    def ARTsum(self):
        S = self.theorem_1()
        best_candidate = self.numeric_case()
        test_cases = 0
        n = 0

        while(True):  # self._running
            most_different = self.distance(test_cases, best_candidate, S)

            test_cases += 1  # number of test cases

            # print(usable_case(best_candidate))  # case

            if (test_cases == 100):  # keeps it running
                print("complete")
                return test_cases

            try:
                global user_function
                user_function(usable_case(best_candidate))
            except:
                n += 1
                print(
                    f"an error occured with input: {usable_case(best_candidate)}")

            # update S
            for i in range(0, self.g):
                S[i][best_candidate[i]] += 1
                k = 3  # number of candidates

                for k in range(0, k):
                    candidate = self.numeric_case()
                    difference = self.distance(test_cases, candidate, S)

                    if (difference > most_different):
                        best_candidate = candidate
                        most_different = difference

                # print(most_different)

            best_candidate = self.numeric_case()



def startButton():
    # user input
    inputs = inputText.get('1.0', tk.END).split('\n')
    code_location = inputs[1]
    function_name = inputs[2]
    valid_input = inputs[3]

    categories = ast.literal_eval(inputs[0])
    non_numeric = outputText.get('1.0', tk.END)

    p = valid_program()
    if p.compile(code_location):

        global user_function
        user_function = p.valid_function(function_name, valid_input)
        if (user_function != None) & transform(non_numeric):

            global c
            c.art.setH(categories)
            c.art.ARTsum()
            c.art._running = True

    statusText.set("Running")
    statusLabel.configure(fg='green')


def stopButton():
    global c
    c.stop()
    c.art._running = False
    statusText.set("Stopped")
    statusLabel.configure(fg='red')


def nextButton():
    None


def writeButton():
    inputText.delete('1.0', tk.END)
    outputText.delete('1.0', tk.END)
    inputText.insert(
        tk.INSERT, "[8, 26, 26, 26, 26, 26, 26, 26, 26]\ntest-me.py\nexample\nstring\n")
    outputText.insert(
        tk.INSERT, 'def usable_case(numeric_case):\n    non_numeric = ""\n    for i in range(1, numeric_case[0] + 2):\n        non_numeric += chr(numeric_case[i] + 97)\n    return non_numeric')

c = CountdownTask()
m = Metronome(c)
t = Thread(target=c.run)
t1 = Thread(target=m.run)
t.start()
t1.start()

# Window
window = tk.Tk()
window.title("CSCI318: Practicing ART")
window.geometry("1000x600")
window.configure(bg='white')

# Labels
NTLabel = tk.Label(window, bg='white', 
                    font=("Helvetica", 14), 
                    text="Number of Tests: ")
RTLabel = tk.Label(window, bg='white', 
                    font=("Helvetica", 14), 
                    text="Rate of Tests: ")
NFLabel = tk.Label(window, bg='white', 
                    font=("Helvetica", 14), 
                    text="Number of Failures: ")
INLabel = tk.Label(window, bg='white', 
                    font=("Helvetica", 14), 
                    text="Input")
OUTLabel = tk.Label(window, bg='white', 
                    font=("Helvetica", 14), 
                    text="Output")

statusText = tk.StringVar()
statusLabel = tk.Label(window, bg='white',
                        font=("Helvetica", 14),
                        textvariable=statusText)

# Textbox
inputText = tk.Text(window, font=("Helvetica", 11), 
                        height=10, 
                        width=40)
outputText = tk.Text(window, font=("Helvetica", 11),
                        height=10, 
                        width=40)

# Entry
NTText = tk.StringVar()
RTText = tk.StringVar()
NFText = tk.StringVar()

NTEntry = tk.Entry(window, font=("Helvetica", 14), 
                    state="readonly",
                    textvariable=NTText)  # number of tests
RTEntry = tk.Entry(window, font=("Helvetica", 14),
                    state="readonly",
                    textvariable=RTText)  # rate of tests
NFEntry = tk.Entry(window, font=("Helvetica", 14),
                    state="readonly",
                    textvariable=NFText)  # number of failures

# Buttons
buttonStart = tk.Button(window, font=("Helvetica", 14), 
                            text="Start", 
                            command=startButton)
buttonStop = tk.Button(window, font=("Helvetica", 14), 
                            text="Stop", 
                            command=stopButton)
buttonWrite = tk.Button(window, font=("Helvetica", 14), 
                            text="Write", 
                            command=writeButton)

buttonPrev = tk.Button(window, font=("Helvetica", 14), text="Previous")  # , command=prevButton)
buttonNext = tk.Button(window, font=("Helvetica", 14), text="Next")  # , command=nextButton)


# Add widgets to grid
NTEntry.grid(row=0, column=1, padx=15, pady=15)
RTEntry.grid(row=1, column=1, padx=15, pady=15)
NFEntry.grid(row=2, column=1, padx=15, pady=15)

NTLabel.grid(row=0, column=0, padx=15, pady=15)
RTLabel.grid(row=1, column=0, padx=15, pady=15)
NFLabel.grid(row=2, column=0, padx=15, pady=15)
INLabel.grid(row=3, column=0, padx=15, pady=15)
OUTLabel.grid(row=3, column=1, padx=15, pady=15)
statusLabel.grid(row=0, column=2, padx=15, pady=15)

inputText.grid(row=4, column=0, padx=15, pady=15)
outputText.grid(row=4, column=1, padx=15, pady=15)

buttonStart.grid(row=2, column=2, padx=15, pady=15)
buttonStop.grid(row=2, column=3, padx=15, pady=15)
buttonPrev.grid(row=5, column=0, padx=15, pady=15)
buttonNext.grid(row=5, column=1, padx=15, pady=15)
buttonWrite.grid(row=1, column=2, padx=15, pady=15)

# Start GUI
window.mainloop()
m.terminate()
c.terminate()
