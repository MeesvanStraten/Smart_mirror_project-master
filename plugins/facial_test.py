import face_recognition
import cv2
import sys
import os  

# open camera
video_capture = cv2.VideoCapture(0)

f=open("./faces/all_names.txt", "r")
fl = f.readlines()
d={}

known_face_encodings = []
known_face_names = []

# foreach name in the all_names.txt document, get a photo in either png or jpg format.
for x in fl:
    if (os.path.isfile("./faces/scanned_photo_"+(x.rstrip())+".png")):
        d["face_{0}".format(x.rstrip())]=face_recognition.load_image_file("./faces/scanned_photo_"+(x.rstrip())+".png")
        d["face_encode_{0}".format(x.rstrip())]=face_recognition.face_encodings(d["face_{0}".format(x.rstrip())])[0]
        known_face_encodings.append(d["face_encode_{0}".format(x.rstrip())])
        known_face_names.append(x.rstrip())
    elif (os.path.isfile("./faces/scanned_photo_"+(x.rstrip())+".jpg")):
        d["face_{0}".format(x.rstrip())]=face_recognition.load_image_file("./faces/scanned_photo_"+(x.rstrip())+".jpg")
        d["face_encode_{0}".format(x.rstrip())]=face_recognition.face_encodings(d["face_{0}".format(x.rstrip())])[0]
        known_face_encodings.append(d["face_encode_{0}".format(x.rstrip())])
        known_face_names.append(x.rstrip())


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                

            face_names.append(name)

            # print and flush the data (to electron)
            print(face_names)
            sys.stdout.flush()

    process_this_frame = not process_this_frame

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()