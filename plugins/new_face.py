import face_recognition
import cv2
import sys

# open camera
camera = cv2.VideoCapture(0)
while True:
    return_value, image = camera.read()

    rgb_frame = image[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_frame)

    # if there are no faces detected, print No_face to eletron. Else save the taken image to the folder and the name to the all_names.txt document
    if not face_locations:
        print("No_face")
        sys.stdout.flush()
    else:
        cv2.imwrite("./plugins/faces/scanned_photo_" + sys.argv[1].rstrip() +'.jpg', image)

        f=open("./plugins/faces/all_names.txt", "a+")
        f.write(sys.argv[1]+"\r\n")
        # delete camera when done
        del(camera)

        # print "done" and flush it to electron
        print("done")
        sys.stdout.flush()

# destroy video capture and all windows
video_capture.release()
cv2.destroyAllWindows()

