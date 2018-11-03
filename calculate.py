import cv2
import numpy as np

def findShape(frame):
    # ret,thresh1 = cv2.threshold(frame,127,255,cv2.THRESH_BINARY)
    _, contours, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


# img=cv2.imread("testResultRight.png",0)
# _, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# print(contours[0])

# hull = cv2.convexHull(cnt)

# areaHull = cv2.contourArea(hull)
# print("Hull area ",areaHull)
# areaCnt = cv2.contourArea(cnt)
# print("Contour area", areaCnt)
# areaRatio = ((areaHull - areaCnt)/areaCnt) * 100 
# print("Ratio", areaRatio)