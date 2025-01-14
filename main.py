import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
from tensorflow import keras
import time

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5","Model/labels.txt")
offset=20
imgSize=300

folder = "data\C"
counter = 0

labels =["A","B","C"]

while True:
    success,img = cap.read()
    hands,img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x,y,w,h = hand['bbox']
        
        imgWhite=np.ones((imgSize,imgSize,3),np.uint8)*255
        imgCrop = img[y-offset:y+h+offset,x-offset:x+w+offset]
        
        aspectRatio = h/w
        
        if aspectRatio>1:
            k = imgSize/h
            wCal = math.ceil(k*w)
            imgResize = cv2.resize(imgCrop,(wCal,imgSize))
            wGap = math.ceil((imgSize-wCal)/2)  
            imgWhite[:,wGap:wCal+wGap]=imgResize
            pred,index=classifier.getPrediction(img)
            print(pred,index)
            
        else:
            k = imgSize/w
            hCal = math.ceil(k*h)
            imgResize = cv2.resize(imgCrop,(imgSize,hCal))
            hGap = math.ceil((imgSize-hCal)/2)  
            imgWhite[hGap:hCal+hGap,:]=imgResize
        
        cv2.imshow("Image Crop",imgCrop)
        cv2.imshow("Image White",imgWhite)
        
    cv2.imshow("Image",img)
    cv2.waitKey(1)
    # key=cv2.waitKey(1)
    # if key == ord("s"):
    #     counter += 1
    #     cv2.imwrite(f"{folder}/Image_{time.time ()}.jpg",imgWhite)
    #     print(counter)