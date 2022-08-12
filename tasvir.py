import cv2
import serial
from time import sleep
import mediapipe as mp
ser = serial.Serial('COM10',9600)
cap = cv2.VideoCapture(0)
facec = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
smile = cv2.CascadeClassifier('mouth.xml')
mpHands = mp.solutions.hands
hands = mpHands.Hands()
ser.writelines(b'H')
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    handgray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resualts = hands.process(handgray)
    faces = facec.detectMultiScale(gray,
                                   scaleFactor=1.1,
                                   minNeighbors=3,
                                   minSize=(30, 30),
                                   flags=cv2.CASCADE_SCALE_IMAGE)
    for x, y, w, h in faces:
        cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)
        smiles = smile.detectMultiScale(gray,
                                        scaleFactor=1.8,
                                        minNeighbors=10)
        sorat = 1
        for sx, sy, sw, sh in smiles:
            sorat = 0
            cv2.rectangle(gray, (sx, sy), (sx + sw, sy + sh), (0, 225, 0), 2)
            print(sorat)
        if sorat == 1:
            if resualts.multi_hand_landmarks == None:
                sorat = 1
                print(sorat)
                print(resualts.multi_hand_landmarks)
                ser.write(b'L')
                sleep(1)
            else:
                sorat = 0
                print(sorat)
                ser.write(b'H')
                sleep(1)
        else:
            sorat = 0
            ser.write(b'H')
            sleep(1)
            print(sorat)









        cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
