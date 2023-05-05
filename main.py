import datetime
import json
import threading
import time
from facialRecognition import FacialRecognition
from communication import Communication
from pinEntry import PinEntry
from savePin import SavePin
from menu import Menu
from gdpr_warning import GdprWarning
from theProdigalProgramReturns import AlarmState


def test_facial_recog():
    faces = FacialRecognition()
    faces.run_facial_recognition()


def pin_entry(comms):
    pin = PinEntry(comms)
    receivemessages = threading.Thread(target=pin.receive_pin, args=())
    receivemessages.start()
    pin.run()
    receivemessages.join()
    pin.root.destroy()

    return pin.passwordCorrect


def save_pin(comms, face_recogniser):
    pin_state = pin_entry(comms)
    print(pin_state)
    if pin_state:
        if face_recogniser.run_facial_recognition():
            SavePin(comms)
        else:
            data = {"verification": "failure"}
            comms.send_message(json.dumps(data))

def runAlarm(comms):
    alarmRunning = True
    alarmScreen = AlarmState(comms)
    while alarmRunning:
        receievemessages = threading.Thread(target=alarmScreen.update_alarm_state, args=())
        receievemessages.start()
        alarmScreen.run()
        receievemessages.join()
        alarmRunning = pin_entry(comms)



def __main__():
    face_recogniser = FacialRecognition()
    comms = Communication(9600)
    while True:
        comms.clear_buffer()
        main_menu = Menu(comms)
        if main_menu.faceRecognition:
            face_recogniser.add_face()
        elif main_menu.changeUsrPin:
            save_pin(comms, face_recogniser)
        elif main_menu.beginAlarm:

        elif main_menu.exitState:
            exit(0)


if __name__ == "__main__":
    __main__()
