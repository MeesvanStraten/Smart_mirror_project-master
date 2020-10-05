import cv2
import face_recognition

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')



def runIdentificationOnWebcam():
    video = cv2.VideoCapture(0)
    while True:
        check, frame = video.read();
        faces = faceCascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)

        for x, y, w, h in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            cv2.imshow("Faces detected", frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                crop_img = frame[y:y + h, x:x + w]
                cv2.imwrite("face1.jpg", crop_img)
                break

def create_new_user():

    video = cv2.VideoCapture(0)
    face_detector = faceCascade
    # For each person, enter one numeric face id
    face_id = input('\n enter user id end press <return> ==>  ')
    # Initialize individual sampling face count
    count = 0
    while True:
        ret, img = video.read()
        #img = cv2.flip(img, -1)  # flip video image vertically
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1
            # Save the captured image into the datasets folder
            cv2.imwrite("backend/facerecognition/faces/User." + str(face_id) + '.' +
                        str(count) + ".jpg", gray[y:y + h, x:x + w])
            cv2.imshow('image', img)
        k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 3:  # Take 30 face sample and stop video
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