

import tkinter as tk
from threading import Thread
import re
import traceback
import ast


def file_string(file_location):
    accumulate = ""

    with open(file_location) as file:
        for line in file:
            accumulate += line

    return accumulate


class user_function:
    def __init__(self, program_location, function_name):
        self.program_location = program_location
        self.function_name = function_name
        self.function = None

    def read(self, label):
        try:
            self.program_string = file_string(self.program_location)

            label['fg'] = 'lime'
            label['text'] = "Successful"

            return True
        except:
            label['fg'] = 'red'
            label['text'] = f"Can't open file '{self.program_location}'"

            return False

    def compile(self, label):
        try:
            exec(self.program_string, locals())

            self.function = eval(self.function_name)

            label['fg'] = 'lime'
            label['text'] = "Successful"

            return True
        except:
            label['fg'] = 'red'
            label['text'] = f"Failed to compile '{self.function_name}'"

            return False

    def test(self, functon_input, label):
        try:
            label['fg'] = 'lime'
            label['text'] = f'Call to {self.function_name}({functon_input}) returned "{self.function(eval(functon_input))}"'

            return True
        except:
            label['fg'] = 'red'
            label['text'] = f'Call to {self.function_name}({functon_input}) caused an error to occur'

            return False

# Get rid of the example conversion label and input box
# Should just be the output label

# Sync the random inputs up

# Figure out something to test

# I can't think of a better way to compile
# Maybe do some research latter


def start_function():
    if(update_function_under_test()):
        if(input_domain(IDELabel)):
            if(update_conversion_function()):
                print("start")  # all the inputs are correct now can start


def stop_function():
    print("stop")


def update_function_under_test():
    PUTELabel['text'] = ""
    FUTELabel['text'] = ""
    EIELabel['text'] = ""

    function_under_test = user_function(
        PUTEntry.get(), FUTEntry.get())  # input, input

    if(function_under_test.read(PUTELabel)):  # label
        if(function_under_test.compile(FUTELabel)):  # label
            # input, label
            return function_under_test.test(EIEntry.get(), EIELabel)

    return False


def update_conversion_function():
    CPELabel['text'] = ""
    CFELabel['text'] = ""
    ECELabel['text'] = ""

    user_conversion_function = user_function(CPEntry.get(), CFEntry.get())

    if(user_conversion_function.read(CPELabel)):
        if(user_conversion_function.compile(CFELabel)):
            return user_conversion_function.test(IDELabel['text'], ECELabel)

    return False

# start calls 
# update then tries to start timer

# get it working then touch up last few usability things


def random_case(input_domain):
    import random

    output_case = []

    # categories = len(input_domain)

    for choices in input_domain:
        output_case.append(random.randrange(0, choices))

    return output_case


def input_domain(label):
    try:
        input_domain = eval(IDEntry.get())

        label['fg'] = 'lime'
        label['text'] = f"{random_case(input_domain)}"

        return True

    except:
        label['fg'] = 'red'
        label['text'] = "Expected an integer list"

        return False


def update(event):
    if(update_function_under_test()):
        if(input_domain(IDELabel)):
            update_conversion_function()


########################################################


# Window
window = tk.Tk()
window.title("CSCI318: Practical ART")
window.geometry("850x600")
window.configure(bg='white')


# PUT = Program Under Test
PUTLabel = tk.Label(window, bg='white',
                    font=("Helvetica", 14),
                    text="Program under test:")

PUTEntry = tk.Entry(window, font=("Helvetica", 14),
                    state="normal")

PUTELabel = tk.Label(window, bg='white',
                     font=("Helvetica", 14))  # , justify=tk.LEFT

PUTLabel.grid(row=0, column=0, padx=15, pady=15)
PUTEntry.grid(row=0, column=1, padx=15, pady=15)
PUTELabel.grid(row=0, column=2, padx=15, pady=15, sticky="w")


# FUT = Function Under Test
FUTLabel = tk.Label(window, bg='white',
                    font=("Helvetica", 14),
                    text="Function under test:")

FUTEntry = tk.Entry(window, font=("Helvetica", 14),
                    state="normal")

FUTELabel = tk.Label(window, bg='white',
                     font=("Helvetica", 14))

FUTLabel.grid(row=1, column=0, padx=15, pady=15)
FUTEntry.grid(row=1, column=1, padx=15, pady=15)
FUTELabel.grid(row=1, column=2, padx=15, pady=15, sticky="w")


# EI = Example Input
EILabel = tk.Label(window, bg='white',
                   font=("Helvetica", 14),
                   text="Example input:")

EIEntry = tk.Entry(window, font=("Helvetica", 14),
                   state="normal")

EIELabel = tk.Label(window, bg='white',
                    font=("Helvetica", 14))

EILabel.grid(row=2, column=0, padx=15, pady=15)
EIEntry.grid(row=2, column=1, padx=15, pady=15)
EIELabel.grid(row=2, column=2, padx=15, pady=15, sticky="w")


# ID = Input Domain
IDLabel = tk.Label(window, bg='white',
                   font=("Helvetica", 14),
                   text="Input domain:")

IDEntry = tk.Entry(window, font=("Helvetica", 14),
                   state="normal")

IDELabel = tk.Label(window, bg='white',
                    font=("Helvetica", 14))

IDLabel.grid(row=3, column=0, padx=15, pady=15)
IDEntry.grid(row=3, column=1, padx=15, pady=15)
IDELabel.grid(row=3, column=2, padx=15, pady=15, sticky="w")


# CP = Conversion Program
CPLabel = tk.Label(window, bg='white',
                   font=("Helvetica", 14),
                   text="Conversion program:")

CPEntry = tk.Entry(window, font=("Helvetica", 14),
                   state="normal")

CPELabel = tk.Label(window, bg='white',
                    font=("Helvetica", 14))

CPLabel.grid(row=4, column=0, padx=15, pady=15)
CPEntry.grid(row=4, column=1, padx=15, pady=15)
CPELabel.grid(row=4, column=2, padx=15, pady=15, sticky="w")


# CF = Conversion Function
CFLabel = tk.Label(window, bg='white',
                   font=("Helvetica", 14),
                   text="Conversion function:")

CFEntry = tk.Entry(window, font=("Helvetica", 14),
                   state="normal")

CFELabel = tk.Label(window, bg='white',
                    font=("Helvetica", 14))

CFLabel.grid(row=5, column=0, padx=15, pady=15)
CFEntry.grid(row=5, column=1, padx=15, pady=15)
CFELabel.grid(row=5, column=2, padx=15, pady=15, sticky="w")


# EC = Example conversion
ECELabel = tk.Label(window, bg='white',
                    font=("Helvetica", 14))

ECELabel.grid(row=6, column=0, padx=15, pady=15, columnspan=3, sticky="w")


# start button
StartButton = tk.Button(window, font=("Helvetica", 14),
                        text="Start",
                        command=start_function)

StartButton.grid(row=7, column=0, padx=15, pady=15)


# stop button
StopButton = tk.Button(window, font=("Helvetica", 14),
                       text="Stop",
                       command=stop_function)

StopButton.grid(row=7, column=1, padx=15, pady=15)


PUTEntry.bind("<Any-KeyRelease>", update)  # bind to any keyrelease
FUTEntry.bind("<Any-KeyRelease>", update)
EIEntry.bind("<Any-KeyRelease>", update)
IDEntry.bind("<Any-KeyRelease>", update)
CPEntry.bind("<Any-KeyRelease>", update)
CFEntry.bind("<Any-KeyRelease>", update)

# Start GUI
window.mainloop()
