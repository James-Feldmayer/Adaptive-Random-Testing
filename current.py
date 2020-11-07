
import tkinter as tk
from threading import Thread
import re
import traceback
import ast

# turn old.py into a library

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


# Figure out something to test

# I can't think of a better way to compile
# Maybe do some research latter


def start_function():
    if(update_gui()):
        print("start")


def stop_function():
    # if running 
    # stop running 

    print("stop")


def clear():
    PUTELabel['text'] = ""
    FUTELabel['text'] = ""
    EIELabel['text'] = ""
    CPELabel['text'] = ""
    CFELabel['text'] = ""
    ECLabel['text'] = ""
    IDELabel['text'] = ""
    TCLabel['text'] = ""


function_under_test = None
user_conversion_function = None

def update_function_under_test():
    global function_under_test
    function_under_test = user_function(PUTEntry.get(), FUTEntry.get())

    if(function_under_test.read(PUTELabel)):
        if(function_under_test.compile(FUTELabel)):
            return function_under_test.test(EIEntry.get(), EIELabel)

    return False


def update_conversion_function():
    global user_conversion_function 
    user_conversion_function = user_function(CPEntry.get(), CFEntry.get())

    if(user_conversion_function.read(CPELabel)):
        if(user_conversion_function.compile(CFELabel)):
            if(user_conversion_function.test(IDELabel['text'], ECLabel)):
            
                # above test ensures this is safe
                conversion_output = user_conversion_function.function(eval(IDELabel['text']))

                global function_under_test 
                function_under_test.test(f'"{conversion_output}"', TCLabel)

                # if function_under_test.test() fails it should not prevent the
                # automated test process from starting 
                
                return True

    return False

# start calls 
# update then tries to start timer

def random_case(input_domain):
    import random

    output_case = []

    # categories = len(input_domain)

    for choices in input_domain:
        output_case.append(random.randrange(0, choices))

    return output_case


def update_input_domain():
    try:
        input_domain = eval(IDEntry.get())

        IDELabel['fg'] = 'lime'
        IDELabel['text'] = f"{random_case(input_domain)}"

        return True

    except:
        IDELabel['fg'] = 'red'
        IDELabel['text'] = "Expected an integer list"

        return False

# move input domain down the bottom
# add label
# remove globals after adding testing

def update_gui():
    clear()

    if(update_function_under_test()):
        if(update_input_domain()):
            return update_conversion_function()

    return False


def update_event(event):
    update_gui()


########################################################


# Window
root = tk.Tk()
root.title("CSCI318: Practical ART")
# root.update_idletasks()
root.geometry("800x500") # "500x500+50+50"
root.configure(bg='white')

# I need to resize many of these elements

# PUT = Program Under Test
PUTLabel = tk.Label(root, bg='white',
                    font=("Helvetica", 14),
                    text="Program under test:")

PUTEntry = tk.Entry(root, font=("Helvetica", 14),
                    state="normal")

PUTELabel = tk.Label(root, bg='white',
                     font=("Helvetica", 14))

PUTLabel.grid(row=0, column=0, padx=15, pady=15)
PUTEntry.grid(row=0, column=1, padx=15, pady=15)
PUTELabel.grid(row=0, column=2, padx=15, pady=15, sticky="w")


# FUT = Function Under Test
FUTLabel = tk.Label(root, bg='white',
                    font=("Helvetica", 14),
                    text="Function under test:")

FUTEntry = tk.Entry(root, font=("Helvetica", 14),
                    state="normal")

FUTELabel = tk.Label(root, bg='white',
                     font=("Helvetica", 14))

FUTLabel.grid(row=1, column=0, padx=15, pady=15)
FUTEntry.grid(row=1, column=1, padx=15, pady=15)
FUTELabel.grid(row=1, column=2, padx=15, pady=15, sticky="w")


# EI = Example Input
EILabel = tk.Label(root, bg='white',
                   font=("Helvetica", 14),
                   text="Example input:")

EIEntry = tk.Entry(root, font=("Helvetica", 14),
                   state="normal")

EIELabel = tk.Label(root, bg='white',
                    font=("Helvetica", 14))

EILabel.grid(row=2, column=0, padx=15, pady=15)
EIEntry.grid(row=2, column=1, padx=15, pady=15)
EIELabel.grid(row=2, column=2, padx=15, pady=15, sticky="w")


# ID = Input Domain
IDLabel = tk.Label(root, bg='white',
                   font=("Helvetica", 14),
                   text="Input domain:")

IDEntry = tk.Entry(root, font=("Helvetica", 14),
                   state="normal")

IDELabel = tk.Label(root, bg='white',
                    font=("Helvetica", 14))

IDLabel.grid(row=3, column=0, padx=15, pady=15)
IDEntry.grid(row=3, column=1, padx=15, pady=15)
IDELabel.grid(row=3, column=2, padx=15, pady=15, sticky="w")


# CP = Conversion Program
CPLabel = tk.Label(root, bg='white',
                   font=("Helvetica", 14),
                   text="Conversion program:")

CPEntry = tk.Entry(root, font=("Helvetica", 14),
                   state="normal")

CPELabel = tk.Label(root, bg='white',
                    font=("Helvetica", 14))

CPLabel.grid(row=4, column=0, padx=15, pady=15)
CPEntry.grid(row=4, column=1, padx=15, pady=15)
CPELabel.grid(row=4, column=2, padx=15, pady=15, sticky="w")


# CF = Conversion Function
CFLabel = tk.Label(root, bg='white',
                   font=("Helvetica", 14),
                   text="Conversion function:")

CFEntry = tk.Entry(root, font=("Helvetica", 14),
                   state="normal")

CFELabel = tk.Label(root, bg='white',
                    font=("Helvetica", 14))

CFLabel.grid(row=5, column=0, padx=15, pady=15)
CFEntry.grid(row=5, column=1, padx=15, pady=15)
CFELabel.grid(row=5, column=2, padx=15, pady=15, sticky="w")


# EC = Example conversion
ECLabel = tk.Label(root, bg='white',
                    font=("Helvetica", 14))

ECLabel.grid(row=6, column=0, padx=15, pady=15, columnspan=3, sticky="w")

# TC = Test conversion
TCLabel = tk.Label(root, bg='white',
                    font=("Helvetica", 14))

TCLabel.grid(row=7, column=0, padx=15, pady=15, columnspan=3, sticky="w")



# start button
StartButton = tk.Button(root, font=("Helvetica", 14),
                        text="Start",
                        command=start_function)

StartButton.grid(row=8, column=0, padx=15, pady=15)


# stop button
StopButton = tk.Button(root, font=("Helvetica", 14),
                       text="Stop",
                       command=stop_function)

StopButton.grid(row=8, column=1, padx=15, pady=15)


# start button
BottomButton = tk.Button(root, font=("Helvetica", 14),
                        text="Start",
                        command=start_function)

BottomButton.grid(row=9, column=0, padx=15, pady=15)


PUTEntry.bind("<Any-KeyRelease>", update_event)  # bind to any keyrelease
FUTEntry.bind("<Any-KeyRelease>", update_event)
EIEntry.bind("<Any-KeyRelease>", update_event)
IDEntry.bind("<Any-KeyRelease>", update_event)
CPEntry.bind("<Any-KeyRelease>", update_event)
CFEntry.bind("<Any-KeyRelease>", update_event)

# Start GUI
root.mainloop()
