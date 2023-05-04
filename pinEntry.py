import time
import tkinter
from tkinter import *
from tkinter import ttk
import json


def callback(P):
    if str.isdigit(P) or len(P) <= 4:
        return True
    else:
        return False


class PinEntry:
    # I hate UX design :)
    root = None
    progressBar = None
    progress = None
    textDisplay = None
    textDisplayBottom = None
    remainingAttempts = None
    entryBox = None
    button = None
    register = None
    passwordCorrect = False
    communication = None

    def __init__(self, comms):
        self.communication = comms
        self.root = Tk()
        self.progress = tkinter.IntVar()
        self.progressBar = ttk.Progressbar(variable=self.progress)
        self.textDisplay = ttk.Label(text='Enter the pin:')
        self.remainingAttempts = ttk.Label(text='Attempts remaining.')
        vcmd = (self.root.register(callback))

        self.entryBox = ttk.Entry(validate='all', validatecommand=(vcmd, '%P'))
        self.button = ttk.Button(text='Submit', command=self.send_pin)

        self.progressBar.place(x=130, y=20, width=200, anchor='center')
        self.textDisplay.place(x=130, y=50, anchor='center')
        self.entryBox.place(x=130, y=70, anchor='center')
        self.button.place(x=130, y=110, anchor='center')
        self.remainingAttempts.place(x=130, y=130, anchor='center')
        self.root.geometry("260x150")
        self.root.title("PIN ENTRY")

    def run(self):
        self.root.mainloop()

    def get_usr_entry(self):
        entry = self.entryBox.get()
        return entry

    def update_progress_bar(self, val):
        self.progress.set(val)

    def update_message(self, val):
        self.textDisplay['text'] = val

    def update_remaining_attempts(self, val):
        self.remainingAttempts['text'] = val

    def send_pin(self):
            pin = self.get_usr_entry()
            data = {"pin": int(pin)}
            self.communication.send_message(json.dumps(data))

    def receive_pin(self):
        while not self.passwordCorrect:
            try:
                data = json.loads(self.communication.get_message())
                print(data)
            except:
                continue
            if 'message' in data:
                if data['message'] == "OUT OF ATTEMPTS":
                    self.passwordCorrect = False
                    self.root.quit()
                    return False
                elif data['message'] == "OUT OF TIME":
                    self.passwordCorrect = False
                    self.root.quit()
                    return False
            elif 'passwordResponse' in data:
                self.update_message(data['passwordResponse'])
                if data['passwordResponse'] == "Correct":
                    self.passwordCorrect = True
                    time.sleep(2)
                    self.root.quit()
                    return True
            self.update_progress_bar((data['timeRemaining']/30000)*100)
            self.update_remaining_attempts("Attempts Remaining: " + str(data['attemptsRemaining']))


