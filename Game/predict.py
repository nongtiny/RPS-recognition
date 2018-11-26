import cv2
from keras.models import load_model
import numpy as np
import os
import evaluate as eva

MODEL_PATH = "myModel04.h5"
img_nameL = "ResultLeft.png"
img_nameR = "ResultRight.png"
model = load_model(MODEL_PATH)
# capp = cv2.VideoCapture(0)
kernel = np.ones((3, 3))/9

capp = cv2.VideoCapture(0)

class Camera(object):
    def __init__(self):
        self.cnt = 0
        self.showL = True
        self.showR = True
        self.mask = None
        self.mask2 = None
        self.toggle = -1
        self.left = ""
        self.right = ""
        self.res = ""
    
    def getToggle(self):
        return self.toggle

    def setToggle(self, t):
        self.toggle = t

    def setShowL(self, s):
        self.showL = s
    
    def setShowR(self, s):
        self.showR = s
        

    def findShape(self, frame):
        # ret,thresh1 = cv2.threshold(frame,127,255,cv2.THRESH_BINARY)
        _, contours, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours


    def showResult(self, left, right):
        cv2.imwrite(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\', left), self.mask2)
        cv2.imwrite(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\', right), self.mask)
        
        imageL, imageR = eva.preProcessImg(left, right)

        (paperL, rockL, scissorL) = model.predict(imageL)[0]
        (paperR, rockR, scissorR) = model.predict(imageR)[0]
        resultLeft, resultRight = eva.finalResult(paperR, rockR, scissorR,paperL, rockL, scissorL)
        return resultLeft, resultRight

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right
    
    def setLeft(self, l):
        self.left = l

    def setRight(self, r):
        self.right = r

    def getResult(self):
        return self.res
    
    def setResult(self, r):
        self.res = r
    
    def whowin(self):
        lw = "Left_win"
        rw = "Right_win"
        tie = "Tie"
        tmpLeft = self.getLeft()
        tmpRight = self.getRight()
        

        if (tmpLeft != "" and tmpRight != ""):
            if ((tmpLeft == "Left_scissor") and (tmpRight == "Right_scissor")) or ((tmpLeft == "Left_rock") and (tmpRight == "Right_rock")) or ((tmpLeft == "Left_paper") and (tmpRight == "Right_paper")):
                self.setResult(tie)
            elif ( (tmpLeft == "Left_scissor" and tmpRight == "") or (tmpLeft == "Left_scissor" and tmpRight == "Right_paper") ):
                self.setResult(lw)
            elif ( (tmpLeft == "Left_paper" and tmpRight == "") or (tmpLeft == "Left_paper" and tmpRight == "Right_rock") ):
                self.setResult(lw)
            elif ( (tmpLeft == "Left_rock" and tmpRight == "") or (tmpLeft == "Left_rock" and tmpRight == "Right_scissor") ):
                self.setResult(lw)
            elif ( (tmpLeft == "" and tmpRight == "Right_paper") or (tmpLeft == "Left_rock" and tmpRight == "Right_paper") ):
                self.setResult(rw)
            elif ( (tmpLeft == "" and tmpRight == "Right_rock") or (tmpLeft == "Left_scissor" and tmpRight == "Right_rock") ):
                self.setResult(rw)
            elif ( (tmpLeft == "" and tmpRight == "Right_scissor") or (tmpLeft == "Left_paper" and tmpRight == "Right_scissor") ):
                self.setResult(rw)

    def run_camera(self):
        _,frameEval = capp.read()
        _,frame = capp.read()
        frame = cv2.flip(frame, 1)
        #Draw box to detect left side
        cv2.rectangle(frame, (0,100), (300,400), (0,255,0), 0)
        #Draw box to detect right side
        cv2.rectangle(frame, (301,100), (640,400), (0,0,255), 0)
        
        roi = frameEval[100:400 , 0:300] #Interest left box area
        roi2 = frameEval[102:400 , 302:640] #Interest right box area

        #Skin color range 
        lower = np.array([0,20,70], dtype = np.uint8)
        upper = np.array([50,255,255], dtype = np.uint8)
        
        #Image Processing and CV
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        self.mask = cv2.inRange(hsv, lower, upper)
        self.mask = cv2.dilate(self.mask, kernel, iterations  = 3)
        self.mask = cv2.GaussianBlur(self.mask, (5,5), 100)

        hsv2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2HSV)
        self.mask2 = cv2.inRange(hsv2, lower, upper)
        self.mask2 = cv2.dilate(self.mask2, kernel, iterations  = 3)
        self.mask2 = cv2.GaussianBlur(self.mask2, (5,5), 100)

        #------- Check is there a hand on the box ------------
        checkL = self.findShape(self.mask)
        checkR = self.findShape(self.mask2)

        # No hand both sides
        if self.getToggle() == 0:
            if not self.showL and not self.showR:
                self.cnt = 0
                frame = cv2.putText(frame, "Left", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                frame = cv2.putText(frame, "Right", (500, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                resultLeft, resultRight = self.showResult(img_nameL, img_nameR)
                self.setLeft(resultLeft)
                self.setRight(resultRight)
                frame = cv2.putText(frame, resultLeft +" " + resultRight, (200, 435), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                print(resultLeft, resultRight)
            if (checkL == [] or len(checkL[0]) < 60 ) and (checkR == [] or len(checkR[0]) < 60 ):
                self.showL = True
                self.showR = True
                frame = cv2.putText(frame, "Put your hands in the box to play", (200, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
            # No hand left side
            elif (checkL == [] or len(checkL[0]) < 60 ):
                self.showL = True
                self.showR = False
                frame = cv2.putText(frame, "Hand is missing on the right side", (200, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
            # No hand right side
            elif (checkR == [] or len(checkR[0]) < 60 ):
                self.showR = True
                self.showL = False
                frame = cv2.putText(frame, "Hand is missing on the left side", (200, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
            #------------- Find Result ----------------------
            else:
                self.cnt+=1
                if(self.cnt > 10):
                    self.showL = False
                    self.showR = False
        cv2.namedWindow("Left")
        cv2.moveWindow("Left", 0,200)
        cv2.namedWindow("Right")
        cv2.moveWindow("Right", 1000,200)
        cv2.namedWindow("GG")
        cv2.moveWindow("GG", 330,150)
        cv2.imshow('GG',frame)
        cv2.imshow('Left',self.mask2)
        cv2.imshow('Right',self.mask)
