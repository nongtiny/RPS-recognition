import numpy as np
import cv2

bgModel = cv2.createBackgroundSubtractorMOG2(0, 50)

def removeBG(frame):
    handmask = bgModel.apply(frame,learningRate=0)
    kernel = np.ones((3, 3))/9
    handmask = cv2.erode(handmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=handmask)
    return res

def processing(frame):
    frame = cv2.bilateralFilter(frame, 5, 50, 100)
    frame = removeBG(frame)
    roi = frame[100:400 , 0:300] #Interest left box area
    roi2 = frame[100:400 , 301:640] #Interest right box area
    
    img = roi
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, left = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)

    img2 = roi2
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    blur2 = cv2.GaussianBlur(gray2, (5, 5), 0)
    ret2, right = cv2.threshold(blur2, 127, 255, cv2.THRESH_BINARY)

    return left,right


    
