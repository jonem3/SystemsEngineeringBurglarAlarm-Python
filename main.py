import datetime
import json
import threading
import time
from facialRecognition import FacialRecognition
from communication import Communication
from pinEntry import PinEntry
from savePin import SavePin


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


def __main__():
    face_recogniser = FacialRecognition()
    comms = Communication(115200)
    # savepin = SavePin(comms)
    save_pin(comms, face_recogniser)


if __name__ == "__main__":
    __main__()
