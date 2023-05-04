import tkinter
from tkinter import *
from tkinter import ttk


class GdprWarning:
    root = None
    yesButton = None
    noButton = None
    message = None
    gdprOutcome = False

    def __init__(self):
        self.root = Tk()
        self.message = ttk.Label(text='GDPR Article 9 requires explicit permission for storing of Biometric Data\nDo '
                                      'you consent to the storage of your Biometric Data?', justify='center')
        buttonHeight = 30
        buttonWidth = 100
        self.yesButton = ttk.Button(text='Yes', command=self.onYes)
        self.noButton = ttk.Button(text='No', command=self.onNo)

        self.message.place(x=200, y=20, anchor='center')
        self.yesButton.place(x=100, y=75, height=buttonHeight, width=buttonWidth, anchor='center')
        self.noButton.place(x=300, y=75, height=buttonHeight, width=buttonWidth, anchor='center')
        self.root.geometry("400x100")
        self.root.title("GDPR Warning")
        self.root.mainloop()

    def onNo(self):
        self.gdprOutcome = False
        self.root.quit()
        self.root.destroy()

    def onYes(self):
        self.gdprOutcome = True
        self.root.quit()
        self.root.destroy()
