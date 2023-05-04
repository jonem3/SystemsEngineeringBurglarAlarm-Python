import tkinter
from tkinter import *
from tkinter import ttk


class Menu:
    root = None
    activateSystem = None
    changePin = None
    registerNewUser = None
    comms = None
    faceRecognition = False
    beginAlarm = False
    changeUsrPin = False
    exitButton = None
    exitState = False

    def __init__(self, comms):
        self.comms = comms
        self.root = Tk()
        self.activateSystem = ttk.Button(text='Activate System', command=self.activate_system)
        self.changePin = ttk.Button(text='Change Pin', command=self.change_pin)
        self.registerNewUser = ttk.Button(text='Register New User', command=self.register_new_user)
        self.exitButton = ttk.Button(text='Exit', command=self.exit)

        buttonHeight = 50
        buttonWidth = 150

        buttonSpacing = buttonHeight*1.1
        screenHeight = (int(buttonSpacing) * 5)
        self.activateSystem.place(x=100, y=buttonSpacing, height=buttonHeight, width=buttonWidth, anchor='center')
        self.changePin.place(x=100, y=buttonSpacing*2, height=buttonHeight, width=buttonWidth, anchor='center')
        self.registerNewUser.place(x=100, y=buttonSpacing*3, height=buttonHeight, width=buttonWidth, anchor='center')
        self.exitButton.place(x=100, y=buttonSpacing*4, height=buttonHeight, width=buttonWidth, anchor='center')

        self.root.geometry("200x"+str(screenHeight))
        self.root.title("Main Menu")
        self.root.mainloop()

    def exit(self):
        self.exitState = True
        self.root.quit()
        self.root.destroy()

    def activate_system(self):
        self.beginAlarm = True
        self.comms.send_message("PO")
        self.root.quit()
        self.root.destroy()

    def change_pin(self):
        self.changeUsrPin = True
        self.comms.send_message("CP")
        self.root.quit()
        self.root.destroy()

    def register_new_user(self):
        self.faceRecognition = True
        self.root.quit()
        self.root.destroy()
