import tkinter as tk
from threading import Thread
import time

# work on interface now
# probably very error prone?

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
        n = 0

        while self._alive:
            if self._running:
                # print(n)
                n += 1

                self.count += 1

    def rate(self):
        if self.s.time_lapsed() == 0:
            return 0

        return int(self.count / self.s.time_lapsed())

class Metronome:
    def __init__(self, c):
        self.c = c  # CountdownTask()
        self._alive = True

    def terminate(self):
        self._alive = False
        self.c.terminate()

    def run(self):
        while self._alive:
            self.c.updateGUI()
            time.sleep(1)

c = CountdownTask()
m = Metronome(c)
t = Thread(target=c.run)
t1 = Thread(target=m.run)
t.start()
t1.start()

def startButton():
    global c
    c.start()
    statusText.set("Running")
    statusLabel.configure(fg='green')

def stopButton():
    global c
    c.stop()
    statusText.set("Stopped")
    statusLabel.configure(fg='red')

# need a currently running indicator

def fastButton():
    None

# Window
window = tk.Tk()
window.title("CSCI318: Practicing ART")
window.geometry("1000x600")
window.configure(bg='white')

# Labels
NTLabel = tk.Label(window, bg='white', font=("Helvetica", 14), text="Number of Tests: ")
RTLabel = tk.Label(window, bg='white', font=("Helvetica", 14), text="Rate of Tests: ")
NFLabel = tk.Label(window, bg='white', font=("Helvetica", 14), text="Number of Failures: ")
INLabel = tk.Label(window, bg='white', font=("Helvetica", 14), text="Input")
OUTLabel = tk.Label(window, bg='white', font=("Helvetica", 14), text="Output")

statusText = tk.StringVar()
statusLabel = tk.Label(window, bg='white',
                        font=("Helvetica", 14),
                        textvariable=statusText)

# Textbox
inputText = tk.Text(window, font=("Helvetica", 11), height=10, width=40)
outputText = tk.Text(window, font=("Helvetica", 11), height=10, width=40)

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
buttonStart = tk.Button(window, font=("Helvetica", 14), text="Start", command=startButton)
buttonStop = tk.Button(window, font=("Helvetica", 14), text="Stop", command=stopButton)
buttonPrev = tk.Button(window, font=("Helvetica", 14), text="Previous")  # , command=prevButton)
buttonNext = tk.Button(window, font=("Helvetica", 14), text="Next")  # , command=nextButton)
buttonFast = tk.Button(window, font=("Helvetica", 14), text="Fast", command=fastButton)
# removed reset button

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
buttonFast.grid(row=1, column=2, padx=15, pady=15)

# Start GUI
window.mainloop()
m.terminate()
