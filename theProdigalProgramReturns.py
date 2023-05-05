import time
import tkinter
from tkinter import *
from tkinter import ttk
import json


class AlarmState:
    # I hate UX design :)
    root = None
    textDisplay = None
    textDisplayBottom = None
    button = None
    passwordEntry = False
    communication = None

    def __init__(self, comms):
        self.communication = comms

        self.root = Tk()
        self.textDisplay = ttk.Label(text='')
        self.textDisplayBottom = ttk.Label(text='')
        self.button = ttk.Button(text='DEACTIVATE', command=self.enter_pin)

        self.textDisplay.place(x=130, y=20, anchor='center')
        self.button.place(x=130, y=110, anchor='center')
        self.textDisplayBottom.place(x=130, y=130, anchor='center')
        self.root.geometry("260x150")
        self.root.title("PIN ENTRY")

    def run(self):
        self.root.mainloop()
        self.communication.send_message("PO")

    def update_message(self, val):
        self.textDisplay['text'] = val

    def update_alarm_state(self, val):
        self.textDisplayBottom['text'] = val

    def enter_pin(self):
        data = "EP"
        self.communication.send_message(data)
        self.passwordEntry = True
        self.root.quit()
        self.root.destroy()

    def receive_data(self):
        while not self.passwordEntry:
            data = json.loads(self.communication.get_message())
            message = ""
            for sensorName, sensorState in data['sensors']:
                message += "Sensor: " + str(sensorName)
                message += "\nState: " + str(sensorState)

            self.update_message(message)

            self.update_alarm_state(data['state'])

