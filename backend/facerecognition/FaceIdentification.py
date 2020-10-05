import cv2

#faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
faceCascade = cv2.CascadeClassifier('data/haarcascade/haarcascade_frontalface_default.xml')

def runIdentificationOnPicture():
    image = cv2.imread("Faces/people.jpg")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30,30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Faces",image)
    cv2.waitKey(0)

def runIdentificationOnWebcam():
    video = cv2.VideoCapture(0)
    while True:
        check, frame = video.read();
        faces = faceCascade.detectMultiScale(frame,scaleFactor=1.1,minNeighbors=5)

        for x, y, w, h in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            cv2.imshow("Faces detected",frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break