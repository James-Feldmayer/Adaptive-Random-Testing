import tkinter as tk
from threading import Thread
import re
import traceback
import ast


"""
0 
need to have some basic gui updates first!

1 
still kind of buggy because I have to open up threads I think

1
work on error handling - robustness

2
report errors to the user when it does not compile (need a good design)

3
write some more examples

4
give full failure information
perhaps create a failure object
that the user can scroll through a list of and display

3 types of failure (all need to be handled)
bad - tester - to command line for james feldmayer
    could be refered to as "logging"
good - input program - full detail option in gui for user
good - unexpected user input - full detail option in gui for user
    traceback.format_exc()
    traceback.print_exc()

###

All of the responsiveness issues are fixed when 

"""

user_function = None

# combine
def transform(user_input_f):
    if type(re.match("def usable_case\(\S*\):", user_input_f)) == re.Match:
        # regex matched

        try:
            exec(user_input_f, globals())  # create usable_case(list)

            try:
                usable_case([7, 7, 6, 3, 13, 1, 22, 18, 17]) # should take user input
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

class ART:
    def __init__(self):
        self.A = [] # user input

        self.S = [] # calculate distance
        self.attempt = 0 # number of test cases
        self.failure = 0

        # private     
        self._running = False
        self._alive = True
     
    def g(self): # number of categories
        return len(self.A)

    def h(self, i): # number of choices
        return len(self.A[i])

    def zeros(self, length):
        vector = []

        for i in range(0, length):
            vector.append(0)

        return vector

    def numeric_case(self):
        import random

        numeric_list = []

        for domain in self.A:
            numeric_list.append(random.randrange(0, domain))

        return numeric_list

    # rate removed as it adds needless complexity

    def updateGUI(self):
        if self.attempt > 0:
            NTText.set(self.attempt)
            NFText.set(self.failure)

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

    def setA(self, A):
        self.A = A
        self.S = self.theorem_1()

    def updateS(self, candidate):
        for i in range(0, self.g()):
            self.S[i][candidate[i]] += 1

    # seems to be implemented correctly
    # what are its dependencies?
        # various functions and datapoints

    # update the GUI !

    # design a new GUI
    def main(self): 

        while self._alive:
            
            if self._running:

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

                self.updateGUI() # could probably use a better name


def startButton():
    # user input
    inputs = inputText.get('1.0', tk.END).split('\n')
    code_location = inputs[1]
    function_name = inputs[2]
    valid_input = inputs[3]

    A = ast.literal_eval(inputs[0])
    non_numeric = outputText.get('1.0', tk.END)

    p = valid_program()
    if p.compile(code_location):

        global user_function
        user_function = p.valid_function(function_name, valid_input)
        if (user_function != None) & transform(non_numeric):

            # 202-216 very ugly

            global c
            c.setA(A) 

            # setup ^ 

            c._running = True

            statusText.set("Running")
            statusLabel.configure(fg='green')


def stopButton():
    global c
    c._running = False

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

# creating the thread causes responsiveness problems but is required

c = ART()
t = Thread(target=c.main)
t.start()

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
c._alive = False
