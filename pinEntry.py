import tkinter
from tkinter import *
from tkinter import ttk


def callback(P):
    if str.isdigit(P) or P == "":
        return True
    else:
        return False


class PinEntry:
    # I hate UX design :)
    root = None
    frame = None
    progressBar = None
    progress = None
    textDisplay = None
    remainingAttempts = None
    entryBox = None
    button = None
    register = None

    def __init__(self):
        self.root = Tk()
        self.frame = ttk.Frame(self.root, padding=10)
        self.progress = tkinter.IntVar()
        self.progressBar = ttk.Progressbar(variable=self.progress)
        self.textDisplay = ttk.Label(text='Enter a pin:')
        self.remainingAttempts = ttk.Label(text='Attempts remaining.')
        vcmd = (self.root.register(callback))

        self.entryBox = ttk.Entry(validate='all', validatecommand=(vcmd, '%P'))
        self.button = ttk.Button(text='Submit')

        self.progressBar.place(x=130, y=20, width=200, anchor='center')
        self.textDisplay.place(x=130, y=50, anchor='center')
        self.entryBox.place(x=130, y=70, anchor='center')
        self.button.place(x=130, y=110, anchor='center')
        self.remainingAttempts.place(x=130, y=130, anchor='center')
        self.root.geometry("260x150")
        self.root.title("PIN DEMO")

    def run(self):
        self.root.mainloop()

    def get_button_state(self):
        state = self.button.state()
        if 'pressed' in state:
            return True
        else:
            return False

    def get_usr_entry(self):
        entry = self.entryBox.get()
        return entry

    def update_progress_bar(self, val):
        self.progress.set(val)

    def update_message(self, val):
        self.textDisplay['text'] = val