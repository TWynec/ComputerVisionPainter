import cv2
import numpy as np
import time 
import os
import HandTrackingModule as htm

# image = cv2.rectangle(image, start_point, end_point, color, thickness) 
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

drawColor = (255,100,0)
brushThickness = 15
eraserThickness = 75
xp, yp = 0,0

imgCanvas = np.zeros((720, 1280, 3), np.uint8)

detector = htm.handDetector(detectionConfidence = 0.85)

while True:
    # Draw when index finger is up
    # Select new color when 2 fingers are up

    success, img = cap.read()
    img = cv2.flip(img,1)

    detector.findHands(img)
    lmList = detector.findPosition(img)

    cv2.rectangle(img, (50,50), (150,100), (255,100,0), cv2.FILLED) 
    cv2.rectangle(img, (200,50), (300,100), (0,0,255), cv2.FILLED) 
    cv2.rectangle(img, (350,50), (450,100), (0,255,0), cv2.FILLED) 
    cv2.rectangle(img, (500,50), (600,100), (0,0,0), cv2.FILLED) 



    if len(lmList) != 0:

        # position of index finger
        x1, y1 = lmList[8][1:]
        # pos of middle finger
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()

        # rectangle is selection mode, circle is drawing mode 
        # select
        if fingers[1] and fingers[2]:
            xp, yp = 0,0
            if y1 < 125:
                if 50<x1<150: # blue
                    drawColor = (255,100,0)
                elif 200<x1<300: # red
                    drawColor = (0,0,255)
                elif 350<x1<450: # green
                    drawColor = (0,255,0)
                elif 500<x1<600: # eraser
                    drawColor = (0,0,0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)
            xp, yp = x1, y1

        #draw
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1



    # add the canvas to the image to see drawing on camera
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)
    #img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)

    cv2.imshow("Image", img)
    #cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1)


