import threading
import tkinter
from tkinter import *
from tkinter import ttk
import tkthread


class TestUi:
    root = None
    frm = None
    progressBar = None
    progress = None
    textDisplay = None

    def __init__(self):
        self.root = Tk()
        self.frm = ttk.Frame(self.root, padding=10)
        self.progress = tkinter.IntVar()
        self.progressBar = ttk.Progressbar(variable=self.progress)
        self.progressBar.place(x=30, y=60, width=200)
        self.textDisplay = ttk.Label(text='')
        self.textDisplay.place(x=30, y=20)
        self.root.geometry("300x200")


    def start(self):
        self.root.mainloop()

    def updateProgressBar(self, val):
        self.textDisplay['text'] = str(round(val, 2)) + "%"
        self.progress.set(val)
