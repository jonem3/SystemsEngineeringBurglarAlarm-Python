import atexit
import csv
import datetime
from os.path import exists
import uuid

import cv2
import os
import numpy as np

"""
Interface:
- Run facial recognition
- Add faces
"""


class FacialRecognition:
    face_recogniser = None
    face_ids = []
    data_folder = "training_data"
    gdpr_warning = "\nGDPR Article 9 requires explicit permission for storing of Biometric Data" \
                   "\nDo you consent to the storage of your Biometric Data? (Y/N) "
    available_faces = []

    def __init__(self):
        self.load_names()
        atexit.register(self.exit_handler)
        self.train_recogniser()

    def train_recogniser(self):
        faces, labels = self.prep_training_data()
        self.face_recogniser = cv2.face.LBPHFaceRecognizer_create()
        self.face_recogniser.train(faces, np.array(labels))

    def locate_face(self, img):
        self.available_faces = []
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faces = face_classifier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=5)
        if len(faces) != 0:
            for i in range(len(faces)):
                (x, y, w, h) = faces[i]
                self.available_faces.append([grey[y:y + w, x:x + h], faces[i]])

    def prep_training_data(self):
        dirs = os.listdir(self.data_folder)
        faces = []
        labels = []
        s_folder = False
        for dir_name in dirs:
            if dir_name.startswith("s"):
                s_folder = True
        if not s_folder:
            print("\nNO BIOMETRIC DATA AVAILABLE\nADD NEW FACE:")
            self.add_face()
            dirs = os.listdir(self.data_folder)

        for dir_name in dirs:
            if not dir_name.startswith("s"):
                continue
            label = int(dir_name.replace("s", ""))
            subject_dir_path = self.data_folder + "/" + dir_name
            subject_image_names = os.listdir(subject_dir_path)
            for image_name in subject_image_names:
                if image_name.startswith("."):
                    continue
                image_path = subject_dir_path + "/" + image_name
                image = cv2.imread(image_path)
                self.locate_face(image)
                if len(self.available_faces) != 0:
                    faces.append(cv2.resize(self.available_faces[0][0], (400, 500)))
                    labels.append(label)
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            cv2.destroyAllWindows()
        return faces, labels

    def classify(self, imtp):
        img = imtp.copy()
        self.locate_face(img)
        recognised_face = None
        if len(self.available_faces) != 0:
            for f in self.available_faces:
                label, conf = self.face_recogniser.predict(cv2.resize(f[0], (400, 500)))
                if conf < 40:
                    (x, y, w, h) = f[1]
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(img, (self.face_ids[label] + " " + str(round(conf, 2))), (f[1][0], f[1][1] - 5),
                                cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
                    recognised_face = self.face_ids[label]
                else:
                    (x, y, w, h) = f[1]
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return img, recognised_face

    def add_face(self):
        webcam = cv2.VideoCapture(0)
        bio_consent = False
        while not bio_consent:
            usr_consent = input(self.gdpr_warning).lower()
            if usr_consent == "y":
                print("\nConsent Acknowledged")
                bio_consent = True
            elif usr_consent == "n":
                print("\nAlarm Shutting Down")
                break
            else:
                print("\nThat was not an available option")
        if bio_consent:
            new_folder_name = "s" + str(len(self.face_ids))
            # new_id = input("\nEnter the name of the person being added: ")
            new_id = str(uuid.uuid4())
            self.face_ids.append(new_id)
            os.mkdir(self.data_folder + "/" + new_folder_name)
            for i in range(1, 25):
                check, frame = webcam.read()
                cv2.imwrite(self.data_folder + "/" + new_folder_name + "/" + str(i) + ".png", frame)
        webcam.release()

    def load_names(self):
        if exists('IDS.csv'):
            with open('IDS.csv', newline='') as csvfile:
                spam_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for row in spam_reader:
                    self.face_ids.append(row[0])

    def new_face_processing(self):
        correct_entry = False
        while not correct_entry:
            choice = input("WOULD YOU LIKE TO ADD A NEW FACE? (Y/N)").lower()
            if choice == "y":
                self.add_face()
                self.train_recogniser()
                correct_entry = True
            elif choice == "n":
                correct_entry = True
            else:
                print("That was not an available option")

    def detect_faces(self, webcam):
        check, frame = webcam.read()
        predicted_img, recog_person = self.classify(frame)
        cv2.imshow("FEED", predicted_img)
        cv2.waitKey(1)

        return recog_person

    def run_facial_recognition(self):
        self.available_faces = []
        start_time = datetime.datetime.now()
        elapsed_time = 0
        webcam = cv2.VideoCapture(0)
        while len(self.available_faces) == 0 and elapsed_time < 30:
            person = self.detect_faces(webcam)
            elapsed_time = (datetime.datetime.now() - start_time).seconds
        cv2.destroyAllWindows()
        webcam.release()
        if person is not None:
            # print(self.available_faces)
            print(str(person).upper(), "RECOGNISED")
            return True
        else:
            print("\nNo one recognised")
            return False

    def exit_handler(self):
        with open('IDS.csv', 'w', newline='') as csvfile:
            spam_writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i in self.face_ids:
                spam_writer.writerow([i])
        cv2.destroyAllWindows()
