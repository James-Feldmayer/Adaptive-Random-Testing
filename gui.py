
import tkinter as tk
from threading import Thread


class CountdownTask:

    def __init__(self):
        self._running = False
        self._alive = True

    def start(self):
        self._running = True

    def stop(self):
        self._running = False

    def terminate(self):
        self._alive = False

    def run(self):
        n = 0

        while self._alive:
            if self._running:
                print(n)
                n += 1


c = CountdownTask()
t = Thread(target=c.run)
t.start()


def startButton():
    global c
    c.start()


def stopButton():
    global c
    c.stop()

#


def resetButton():
    print("Hello World ")


# Window
window = tk.Tk()
window.title("CSCI318: Practicing ART")
window.geometry("900x500")

# Labels
NTLabel = tk.Label(window, text="Number of Tests: ")
RTLabel = tk.Label(window, text="Rate of Tests: ")
NFLabel = tk.Label(window, text="Number of Failures: ")
INLabel = tk.Label(window, text="Input")
OUTLabel = tk.Label(window, text="Output")

# Textbox
inputText = tk.Text(window, height=10, width=40)
outputText = tk.Text(window, height=10, width=40)

# Input
NTEntry = tk.Entry(window)  # number of tests
RTEntry = tk.Entry(window)  # rate of tests
NFEntry = tk.Entry(window)  # number of failures
NTEntry.config(state='disabled')
RTEntry.config(state='disabled')
NFEntry.config(state='disabled')

# Buttons
buttonStart = tk.Button(window, text="Start", command=startButton)
buttonStop = tk.Button(window, text="Stop", command=stopButton)
buttonPrev = tk.Button(window, text="Previous")  # , command=prevButton)
buttonNext = tk.Button(window, text="Next")  # , command=nextButton)

# difficult
# using it to do something else for the time being
buttonReset = tk.Button(window, text="Reset")  # , command=resetButton)

# Add widgets to grid
NTLabel.grid(row=0, column=0, padx=15, pady=15)
NTEntry.grid(row=0, column=1, padx=15, pady=15)
RTLabel.grid(row=1, column=0, padx=15, pady=15)
RTEntry.grid(row=1, column=1, padx=15, pady=15)
NFLabel.grid(row=2, column=0, padx=15, pady=15)
NFEntry.grid(row=2, column=1, padx=15, pady=15)
INLabel.grid(row=3, column=0, padx=15, pady=15)
OUTLabel.grid(row=3, column=1, padx=15, pady=15)
inputText.grid(row=4, column=0, padx=15, pady=15)
outputText.grid(row=4, column=1, padx=15, pady=15)
buttonStart.grid(row=1, column=2, padx=15, pady=15)
buttonStop.grid(row=1, column=3, padx=15, pady=15)
buttonPrev.grid(row=5, column=0, padx=15, pady=15)
buttonNext.grid(row=5, column=1, padx=15, pady=15)
buttonReset.grid(row=0, column=2, padx=15, pady=15)

# Start GUI
window.mainloop()
c.terminate()
