import datetime
import time
from facialRecognition import FacialRecognition
from communication import Communication
from pinEntry import PinEntry


def test_facial_recog():
    faces = FacialRecognition()
    faces.run_facial_recognition()


def polling_active(comms):
    comms.send_message("PO CONFIRM")
    polling = True
    print("SYSTEM ACTIVATED: YOU HAVE 5 SECONDS TO EXIT THE PREMISES")
    lastEvent = datetime.datetime.now()
    while polling:
        arduinoCommand = comms.get_message()
        if arduinoCommand == "PIR TRIGGERED":
            print("MOVEMENT DETECTED")
            comms.send_message("ST CONFIRM")
            lastEvent = datetime.datetime.now()
        elif arduinoCommand == "DOOR TRIGGERED":
            print("DOOR HAS BEEN OPENED")
            comms.send_message("ST CONFIRM")
            lastEvent = datetime.datetime.now()
        elif arduinoCommand == "PIN REQUIRED":
            pass  # Enter Pin
        elif arduinoCommand == "PD":
            polling = False
            comms.send_message("PD CONFIRM")
        elif arduinoCommand == "AA":
            polling = False
            pass  # Trigger Alarm
        elif (datetime.datetime.now() - lastEvent).seconds >= 5:
            lastEvent = datetime.datetime.now()
            print("NO SENSOR DETECTION")

def comms_handler(comms, face_recogniser):
    while True:
        arduinoCommand = comms.get_message()
        if arduinoCommand == "AM":
            # menu()
            pass
        elif arduinoCommand == "FR":
            face_recognised = face_recogniser.run_facial_recognition()



def __main__():
    pin = PinEntry()
    pin.run()
    face_recogniser = FacialRecognition()
    comms = Communication(115200)
    comms.send_message("COMPLETE")
    comms.get_message()


if __name__ == "__main__":
    __main__()
