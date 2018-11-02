import cv2
from keras.models import load_model
from imutils.video import VideoStream
from threading import Thread
import numpy as np
import imutils
import time
import os
import evaluate as eva

MODEL_PATH = "myModel02.h5"
model = load_model(MODEL_PATH)
capp = cv2.VideoCapture(0)
capp2 = cv2.VideoCapture(0)
time.sleep(2.0)
kernel = np.ones((3, 3))/9

def removeBG(frame):
    handmask = bgModel.apply(frame,learningRate=0)
    kernel = np.ones((3, 3))/9
    handmask = cv2.erode(handmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=handmask)
    return res


while True:
    ret,frameEval = capp.read()
    ret2,frame = capp.read()
    cv2.rectangle(frame, (0,100), (300,400), (0,255,0), 0)
    #Draw box to detect right side
    cv2.rectangle(frame, (301,100), (640,400), (0,0,255), 0)
    
    roi = frameEval[100:400 , 0:300] #Interest left box area
    roi2 = frameEval[100:400 , 301:640] #Interest right box area

    lower = np.array([0,20,70], dtype = np.uint8)
    upper = np.array([20,255,255], dtype = np.uint8)
    
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.dilate(mask, kernel, iterations  = 3)
    mask = cv2.GaussianBlur(mask, (5,5), 100)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    hsv2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2HSV)
    mask2 = cv2.inRange(hsv2, lower, upper)
    mask2 = cv2.dilate(mask2, kernel, iterations  = 3)
    mask2 = cv2.GaussianBlur(mask2, (5,5), 100)
    mask2 = cv2.cvtColor(mask2, cv2.COLOR_GRAY2BGR)


    # frameEval = cv2.bilateralFilter(frameEval, 5, 50, 100)
    # frameEval = removeBG(frameEval)
    # roi = frameEval[100:400 , 0:300] #Interest left box area
    # roi2 = frameEval[100:400 , 301:640] #Interest right box area
    
    # img = roi
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # ret, left = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)
    # left = cv2.cvtColor(left, cv2.COLOR_GRAY2BGR)

    # img2 = roi2
    # gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # blur2 = cv2.GaussianBlur(gray2, (5, 5), 0)
    # ret2, right = cv2.threshold(blur2, 60, 255, cv2.THRESH_BINARY)
    # right = cv2.cvtColor(right, cv2.COLOR_GRAY2BGR)

    (leftFrame, rightFrame) = eva.preProcessImg(mask,mask2)

    (paperL, rockL, scissorL) = model.predict(leftFrame)[0]
    (paperR, rockR, scissorR) = model.predict(rightFrame)[0]
    resultLeft, resultRight = eva.finalResult(paperL, rockL, scissorL, paperR, rockR, scissorR)

    frame = cv2.putText(frame, resultLeft, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    frame = cv2.putText(frame, resultRight, (500, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow('GG',frame)
    cv2.imshow('left',mask)
    cv2.imshow('right',mask2)

    k = cv2.waitKey(1)
    if k == 27:  # press ESC to exit
        break

capp.release()
cv2.destroyAllWindows()
