import json
import time
import cv2
import face_recognition
import os
from backend.Database import *
import numpy as np # Import Numpy library
from backend.voicerecognition.voicerecognition import *

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def poc_auto_face_tracking():
    video = cv2.VideoCapture(0)
    face_detector = faceCascade

    count = 0
    while True:
        ret, img = video.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1
            gray = cv2.resize(gray[y:y + h, x:x + w], (128, 128), interpolation=cv2.INTER_AREA)
            cv2.imshow('image', img)

        k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break
    video.release()
    cv2.destroyAllWindows()


def poc_manual_tracking():
    cap = cv2.VideoCapture(0)

    # Create the background subtractor object
    # Use the last 700 video frames to build the background
    back_sub = cv2.createBackgroundSubtractorMOG2(history=700,
                                                  varThreshold=25, detectShadows=True)

    # Create kernel for morphological operation
    # You can tweak the dimensions of the kernel
    # e.g. instead of 20,20 you can try 30,30.
    kernel = np.ones((20, 20), np.uint8)

    while (True):

        # Capture frame-by-frame
        # This method returns True/False as well
        # as the video frame.
        ret, frame = cap.read()

        # Use every frame to calculate the foreground mask and update
        # the background
        fg_mask = back_sub.apply(frame)

        # Close dark gaps in foreground object using closing
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

        # Remove salt and pepper noise with a median filter
        fg_mask = cv2.medianBlur(fg_mask, 5)

        # Threshold the image to make it either black or white
        _, fg_mask = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY)

        # Find the index of the largest contour and draw bounding box
        fg_mask_bb = fg_mask
        contours, hierarchy = cv2.findContours(fg_mask_bb, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        areas = [cv2.contourArea(c) for c in contours]

        # If there are no countours
        if len(areas) < 1:

            # Display the resulting frame
            cv2.imshow('frame', frame)

            # If "q" is pressed on the keyboard,
            # exit this loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Go to the top of the while loop
            continue

        else:
            # Find the largest moving object in the image
            max_index = np.argmax(areas)

        # Draw the bounding box
        cnt = contours[max_index]
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # Draw circle in the center of the bounding box
        x2 = x + int(w / 2)
        y2 = y + int(h / 2)
        cv2.circle(frame, (x2, y2), 4, (0, 255, 0), -1)

        # Print the centroid coordinates (we'll use the center of the
        # bounding box) on the image
        text = "x: " + str(x2) + ", y: " + str(y2)
        cv2.putText(frame, text, (x2 - 10, y2 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # If "q" is pressed on the keyboard,
        # exit this loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close down the video stream
    cap.release()
    cv2.destroyAllWindows()



def create_new_user(name: str):

    video = cv2.VideoCapture(0)
    face_detector = faceCascade

    # Create user in database and retrieve the ID generated to save the image to.
    # name = command_listen_to_name()
    insert_new_user(name)
    user_result = get_user_by_name(name)
    face_id = user_result[0].doc_id
    # Initialize individual sampling face count
    count = 0
    while True:
        ret, img = video.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1
            gray = cv2.resize(gray[y:y + h, x:x + w], (128, 128), interpolation=cv2.INTER_AREA)
            cv2.imwrite("backend/facerecognition/faces/User." + str(face_id) + ".jpg", gray)
            cv2.imshow('image', img)

        k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 1:
            break

    video.release()
    cv2.destroyAllWindows()


def compare_faces(img1_path :str, img2_path:str):
    img1 = face_recognition.load_image_file(img1_path)
    img2 = face_recognition.load_image_file(img2_path)

    img1_encoding = face_recognition.face_encodings(img1)[0]
    img2_encoding = face_recognition.face_encodings(img2)[0]

    results = face_recognition.compare_faces([img1_encoding], img2_encoding)

    return results



def find_user_face():
    #calls function to create a temp image of user
    capture_user_face()

    #image created by capture_user_face(), gets deleted after the encoding for safety
    user_to_login = face_recognition.load_image_file("backend/facerecognition/TempUser.jpg")

    path = "backend/facerecognition/faces"

    known_faces_paths = []
    known_faces_encodings = []

    if not user_to_login.any():
        print("user_to_login img is not loaded correctly..")

    for subdir, dirs, files in os.walk(path):
        for file in files:
            known_faces_paths.append(os.path.join(subdir, file))

    #encodes each face in the from know_faces array to encoding array
    for face_path in known_faces_paths:
        known_faces_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(face_path))[0])

    #encodes user_to_login and removes after encoding
    if not face_recognition.face_encodings(user_to_login):
        print("Not possible to encode face from img")
        os.remove("backend/facerecognition/TempUser.jpg")
    else:
        user_to_login_encoding = face_recognition.face_encodings(user_to_login)[0]
        if not user_to_login_encoding.any():
            print("No face detected")
            os.remove("backend/facerecognition/TempUser.jpg")
        else:
            results = face_recognition.compare_faces(known_faces_encodings, user_to_login_encoding)
            os.remove("backend/facerecognition/TempUser.jpg")

            #return array of booleans True = user_to_login is the same as person as N in array
            return results


#This function captures a temp image of the user in front of the camera which is used in the find_user_face() function
def capture_user_face():
    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    count = 0
    while True:
        check, frame = video.read()
        faces = faceCascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)

        for x, y, w, h in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            count += 1
            crop_img = frame[y:y + h, x:x + w]
            crop_img = cv2.resize(crop_img, (128,128), interpolation = cv2.INTER_AREA)

            cv2.imwrite("backend/facerecognition/TempUser" + ".jpg", crop_img)
        #3 frames, overwrites each time
        if count >= 3:
            break;