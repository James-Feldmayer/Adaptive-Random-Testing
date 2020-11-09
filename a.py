import tkinter as tk
from tkinter import ttk


root = tk.Tk()

root.title("Python Tkinter Text Box")
root.minsize(600, 400)


def clickMe():
    text.insert('1.0', "ello' wrld \n")


# print(text.get('1.0', 'end-1c'))

text = tk.Text(root, height=8, width=20)
text.grid(column=0, row=0)

# T.insert(tk.END, "Just a text Widget\nin two lines\n")

button = ttk.Button(root, text="Click Me", command=clickMe)
button.grid(column=0, row=1)

root.mainloop()
