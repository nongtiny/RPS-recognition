import cv2
from keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import evaluate as eva
import calculate as cal

MODEL_PATH = "myModel04.h5"
model = load_model(MODEL_PATH)
capp = cv2.VideoCapture(0)
capp2 = cv2.VideoCapture(0)
kernel = np.ones((3, 3))/9

cntL_P = 0
cntL_R = 0
cntL_S = 0
cntR_P = 0
cntR_R = 0
cntR_S = 0
enough = 50
realLeft=''
realRight=''
tmpL = ''
tmpR = ''

showL = True
showR = True


while True:
    ret,frameEval = capp.read()
    ret2,frame = capp.read()
   
    #Draw box to detect left side
    cv2.rectangle(frame, (0,100), (300,400), (0,255,0), 0)
    #Draw box to detect right side
    cv2.rectangle(frame, (301,100), (640,400), (0,0,255), 0)
    
    roi = frameEval[100:400 , 0:300] #Interest left box area
    roi2 = frameEval[102:400 , 302:640] #Interest right box area

    #Skin color range 
    lower = np.array([0,20,70], dtype = np.uint8)
    upper = np.array([20,255,255], dtype = np.uint8)
    
    #Image Processing and CV
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.dilate(mask, kernel, iterations  = 3)
    mask = cv2.GaussianBlur(mask, (5,5), 100)

    hsv2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2HSV)
    mask2 = cv2.inRange(hsv2, lower, upper)
    mask2 = cv2.dilate(mask2, kernel, iterations  = 3)
    mask2 = cv2.GaussianBlur(mask2, (5,5), 100)

    #Train frame
    trainL = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    trainR = cv2.cvtColor(mask2, cv2.COLOR_GRAY2BGR)
   
    #--------- Prediction ----------
    (leftFrame, rightFrame) = eva.preProcessImg(trainL,trainR)
    (paperL, rockL, scissorL) = model.predict(leftFrame)[0]
    (paperR, rockR, scissorR) = model.predict(rightFrame)[0]
    resultLeft, resultRight = eva.finalResult(paperL, rockL, scissorL, paperR, rockR, scissorR)

    #------- Check is there a hand on the box ------------
    checkL = cal.findShape(mask)
    checkR = cal.findShape(mask2)

    # No hand both sides
    if (checkL == [] or len(checkL[0]) < 150 ) and (checkR == [] or len(checkR[0]) < 150 ):
        showL = True
        showR = True
        cntL_P = 0
        cntL_R = 0
        cntL_S = 0
        cntR_P = 0
        cntR_R = 0
        cntR_S = 0

    # No hand left side
    elif (checkL == [] or len(checkL[0]) < 150 ):
        showL = True
        showR = False
        cntL_P = 0
        cntL_R = 0
        cntL_S = 0
        cntR_P = 0
        cntR_R = 0
        cntR_S = 0

    # No hand right side
    elif (checkR == [] or len(checkR[0]) < 150 ):
        showR = True
        showL = False
        cntL_P = 0
        cntL_R = 0
        cntL_S = 0
        cntR_P = 0
        cntR_R = 0
        cntR_S = 0
         
    #------------- Find Result ----------------------
    else:
        showL = False
        showR = False
        if cntL_P == enough or cntL_R == enough or cntL_S == enough:
            realLeft = tmpL
        elif resultLeft == "Left paper":
            cntL_P+=1
            tmpL = "Paper"
        elif resultLeft == "Left rock":
            cntL_R+=1
            tmpL = "Rock"
        elif resultLeft == "Left scissor":
            cntL_S+=1
            tmpL = "Scissor"

        if cntR_P == enough or cntR_R == enough or cntR_S == enough:
            realRight = tmpR
        elif resultRight == "Right paper":
            cntR_P+=1
            tmpR = "Paper"
        elif resultRight == "Right rock":
            cntR_R+=1
            tmpR = "Rock"
        elif resultRight == "Right scissor":
            cntR_S+=1
            tmpR = "Scissor"

    #--------- Show Result -------------------

    if not showL and not showR:
        frame = cv2.putText(frame, "Left", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        frame = cv2.putText(frame, "Right", (500, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    elif not showL:
        frame = cv2.putText(frame, "Hand missing on the right side", (200, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    elif not showR:
        frame = cv2.putText(frame, "Hand missing on the left side", (200, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        frame = cv2.putText(frame, "Put your hands in the box to play", (200, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    #------ Final Result --------
    if realLeft != '' and realRight != '':
        frame = cv2.putText(frame, realLeft +" " + realRight, (200, 435), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    cv2.imshow('GG',frame)
    cv2.imshow('left',mask)
    cv2.imshow('right',mask2)


    k = cv2.waitKey(1)
    if k == 27:  # press ESC to exit
        break

capp.release()
cv2.destroyAllWindows()
