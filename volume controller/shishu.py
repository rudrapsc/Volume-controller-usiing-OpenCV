import cv2
import numpy as np
import time
import os
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from cvzone.HandTrackingModule import HandDetector
import webbrowser
import AppOpener
import wmi
import pyttsx3
b=0
d=0
c=0
e=0
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
area = 0
colorVol = (255, 0, 0)

detector =HandDetector(detectionCon=0.5,maxHands=4)

while True:
    success, img = cap.read()
    hands,img=detector.findHands(img,flipType=True)

    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        # bbox1 = hand1["bbox"]
        # centerPoint1 = hand1['center']
        # handType1 = hand1["type"]

        fingers = detector.fingersUp(hand1)
        c = 0
        for i in range(5):
            if (fingers[i] == 1):
                c = c + 1
        cv2.putText(img,f'count:{c}',(40,70),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),3)
        if len(hands) == 1:
            print(c)
        if c==3:
            e=3
        if e==3:
            if len(hands)==1:
                length, Info, img = detector.findDistance(lmList1[8][0:2], lmList1[4][0:2], img)
                volBar = np.interp(length, [50, 200], [400, 150])
                volPer = np.interp(length, [50, 200], [0, 100])
                smoothness = 10
                if not fingers[4]:
                    volume.SetMasterVolumeLevelScalar(volPer / 100, None)
                    # cv2.circle(img, (Info[4], Info[5]), 15, (0, 255, 0), cv2.FILLED)
                    # colorVol = (0, 255, 0)
                else:
                    colorVol = (255, 0, 0)
                cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
                cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
                cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                            1, (255, 0, 0), 3)
                cVol = int(volume.GetMasterVolumeLevelScalar() * 100)
                cv2.putText(img, f'Vol Set: {int(cVol)}', (400, 50), cv2.FONT_HERSHEY_COMPLEX,
                                1, colorVol, 3)
            print(fingers)
        if c==5:
            e=0
        if c == 1:
             if d== 0:
                if c == 1:
                    pyttsx3.speak("opening")
                    p = webbrowser.open('http://www.google.com')
                    d = 1
                p=webbrowser.open('http://www.google.com')
        # 
        if len(hands) == 2:
            # Hand 2
            hand2 = hands[1]
            # lmList2 = hand2["lmList"]
            # bbox2 = hand2["bbox"]
            # centerPoint2 = hand2['center']
            # handType2 = hand2["type"]

            fingers2 = detector.fingersUp(hand2)
            # length, Info, img = detector.findDistance(lmList1[8][0:2], lmList2[8][0:2], img)
            # volBar = np.interp(length, [50, 200], [400, 150])
            # volPer = np.interp(length, [50, 200], [0, 100])
            # smoothness = 10
            # print(fingers2)
            for i in range(5):
                if (fingers2[i]==1):
                    c = c + 1

            print(c)

            if b==0:
                if c==1:
                    AppOpener.run("notepad")
                    h="notepad"
                    time.sleep(2)
                    b=1



    cv2.imshow("Image", img)
    f = cv2.waitKey(1)


    if f == ord('g'):
        cv2.destroyAllWindows()
        break