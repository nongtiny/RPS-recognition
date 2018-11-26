import cv2
from keras.preprocessing.image import img_to_array
import numpy as np


def preProcessImg(leftPic, rightPic ):
    #imageL = cv2.imread("resultLeft.png") # put Left img file here
    imageL = cv2.imread(rightPic)
    imageL = cv2.resize(imageL, (28, 28))
    imageL = imageL.astype("float")
    imageL = img_to_array(imageL)
    imageL = np.expand_dims(imageL, axis=0)

    imageR = cv2.imread(leftPic) # put Right img file here
    imageR = cv2.resize(imageR, (28, 28))
    imageR = imageR.astype("float")
    imageR = img_to_array(imageR)
    imageR = np.expand_dims(imageR, axis=0)
    return (imageL,imageR)


def finalResult(paperL, rockL, scissorL, paperR, rockR, scissorR):
    left = ""
    right = ""
    if paperL > 0:
        left = "Left_paper"
    elif rockL > 0:
        left = "Left_rock"
    elif scissorL > 0:
        left = "Left_scissor"  

    if paperR > 0:
        right = "Right_paper"
    elif rockR > 0:
        right = "Right_rock"
    elif scissorR > 0:
        right = "Right_scissor" 
    return (left,right)
