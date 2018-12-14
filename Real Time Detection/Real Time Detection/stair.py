import numpy as np
import cv2
import textspeech
import os

x = 'stairhaarcascade_stage'+str(24)+'.xml'
face_cascade = cv2.CascadeClassifier(x)



def main(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        print("stair")
        os.system("mpg321 stair.mp3")
        

    
