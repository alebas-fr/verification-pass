#!/usr/bin/env python
# coding: utf-8

# Importation de librairies


import cv2
from pyzbar.pyzbar import decode
import pyqrcode
import webbrowser
from pyqrcode import QRCode


def CameraOpen(Camfx = 0.5, Camfy=0.5):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened(): #cas d'erreur
        raise IOError("Cannot open webcam")
        
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=Camfx, fy=Camfy, interpolation=cv2.INTER_AREA)
        cv2.imshow('Input', frame)
        c = cv2.waitKey(1) #echap
        if c == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

get_ipython().system('pip install pyzbar')
get_ipython().system('pip install pyzbar[scripts]')



def QRCodeDetection(Camfx = 0.5, Camfy=0.5):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened(): #cas d'erreur
        raise IOError("Cannot open webcam")
        
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=Camfx, fy=Camfy, interpolation=cv2.INTER_AREA)
        for barcode in decode(frame):
            print(barcode.data)
            myData = barcode.data.decode('utf-8')
            print(myData)
            cv2.imshow('Input',frame)
            c = cv2.waitKey(1)
    cap.release()
    cv2.destroyAllWindows()


cap = cv2.VideoCapture(0)
detector =cv2.QRCodeDetector()
while True:
    _,img = cap.read()
    data,one, _ = detector.detectAndDecode(img)
    if data:
        a = data
        print(a)
        break
    cv2.imshow('qrcodescanner app',img)
    if cv2.waitKey(1)==ord('q'):
        break
b =webbrowser.open(str(a))
cap.release(a)
cv2.destroyAllWindows





