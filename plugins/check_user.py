import face_recognition
import cv2
import sys
import os  
import time

video_capture = cv2.VideoCapture(0)

no_face = 0

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    face_locations = face_recognition.face_locations(frame)
    # cv2.imshow('original', frame)

    if not face_locations:
        no_face = no_face + 1
        time.sleep(5)
    else:
        no_face = 0

    if no_face == 4:
        no_face = 0
        print("logout") 

    print(no_face)
    sys.stdout.flush()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()