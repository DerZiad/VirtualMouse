import numpy as np
import HandTrackingModule as htm
import math
import cv2
import HandTrackingModule
from pynput.mouse import Controller,Button
import ctypes
import time

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
maxwidth = screensize[0]
maxheigth = screensize[1]
mouse = Controller()
detector = HandTrackingModule.handDetector(maxHands=1,detectionCon=0.7)
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
tipIds = [4, 8, 12, 16, 20]

oldx1 = maxwidth // 2
oldy1 = maxheigth // 2
scrolling = False
mouse.position = (oldx1,oldy1)
dpi = 4
while True:
    pTime = time.time()
    success, img = cap.read()
    if success:
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        if len(lmList) != 0:

            fingers = []
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            totalFingers = fingers.count(1)
            if totalFingers == 5:
                mouse.press(Button.left)
                mouse.release(Button.left)
                time.sleep(0.6)
            elif totalFingers == 4:
                mouse.press(Button.right)
                mouse.release(Button.right)
                time.sleep(0.6)
            elif totalFingers == 2 or totalFingers == 1:
                finger = lmList[8]
                x = finger[1]
                y = finger[2]

                xScreenPos = (x - oldx1)*dpi
                yScreenPos = (y - oldy1)*dpi

                oldx1 = x
                oldy1 = y
                mouse.move(xScreenPos, yScreenPos)



        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255, 0, 0), 3)

        cv2.imshow("Img", img)
        cv2.waitKey(1)
