import tkinter
import json

from tkinter import *
from tkinter import ttk


def callback(P):
    if str.isdigit(P) or len(P) <= 4:
        return True
    else:
        return False

class SavePin:
    root = None
    entryBox = None
    button = None
    text = None
    previous = None

    def __init__(self, comms):
        self.comms = comms
        self.root = Tk()
        self.text = ttk.Label(text='Enter a new pin:')
        vcmd = (self.root.register(callback))
        self.entryBox = ttk.Entry(validate='all', validatecommand=(vcmd, '%P'))
        self.button = ttk.Button(text='Submit', command=self.check_entry)

        self.entryBox.place(x=130, y=70, anchor='center')
        self.text.place(x=130, y=50, anchor='center')
        self.button.place(x=130, y=110, anchor='center')
        self.root.geometry("260x150")
        self.root.title("PIN CHANGE")
        self.root.mainloop()

    def check_entry(self):
        if self.previous is None:
            self.previous = int(self.entryBox.get())
            self.text['text'] = "Re-Enter Pin:"
            self.entryBox.delete(0, END)
        else:
            if int(self.entryBox.get()) == self.previous:
                data = {"verification": "success", "newPin": self.previous}
                self.comms.send_message(json.dumps(data))
                self.root.quit()
                self.root.destroy()
            else:
                self.text['text'] = 'Mismatch, Enter a new pin:'
                self.previous = None
                self.entryBox.delete(0, END)

