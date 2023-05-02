import sys
import time

from facialRecognition import FacialRecognition
from communication import Communication
from pinEntry import PinEntry
import threading
import json


def test_facial_recog():
    for i in range(0, 100):
        time.sleep(2)
    faces = FacialRecognition()
    faces.run_facial_recognition()


def test_communication(interface):
    comms = Communication(9600)

    while True:
        jsonData = comms.get_message()
        irDistance = jsonData["IRSensors"][0]["value"]
        distance = 0.0001 * (irDistance * irDistance) - 0.1439 * (irDistance) + 49.9653 + 4
        interface.updateProgressBar(distance)


def read_button(interface, comms):
    previous_state = False
    while True:
        while interface.get_button_state():
            if not previous_state:
                previous_state = True
                message = {"pin": str(interface.get_usr_entry())}
                print(message)
                comms.send_message(message)
        previous_state = False


def process_arduino_pin_entry(interface, comms):
    while True:
        current_data = comms.get_message()
        if 'pinData' in current_data:
            timeElapsed = current_data['pinData'][0]['TimeRemaining'] / 1000
            availTime = current_data['pinData'][0]['AvailTime']
            interface.update_progress_bar((timeElapsed / availTime) * 100)
        elif 'pinResponse' in current_data:
            state = current_data['pinResponse']
            interface.update_message(state)


def __main__():
    user_interface = PinEntry()
    comms = Communication(9600)
    threading.Thread(target=read_button, args=(user_interface, comms,)).start()
    threading.Thread(target=process_arduino_pin_entry, args=(user_interface, comms,)).start()
    user_interface.run()


if __name__ == "__main__":
    __main__()
