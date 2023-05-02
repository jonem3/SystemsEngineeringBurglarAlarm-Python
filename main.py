import time
from facialRecognition import FacialRecognition
from communication import Communication
from pinEntry import PinEntry


def test_facial_recog():
    faces = FacialRecognition()
    faces.run_facial_recognition()


def __main__():
    face_recogniser = FacialRecognition()
    comms = Communication(115200)
    comms.send_message("COMPLETE")
    if comms.get_message() == "COMPLETE CONFIRM":
        print("YAY!")

if __name__ == "__main__":
    __main__()
