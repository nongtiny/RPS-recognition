import cv2
import os
import numpy as np

img=cv2.imread("result.png",0)
ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
_, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnt = max(contours, key = lambda x: cv2.contourArea(x))

print(cnt)

hull = cv2.convexHull(cnt)

areaHull = cv2.contourArea(hull)
print("Hull area ",areaHull)
areaCnt = cv2.contourArea(cnt)
print("Contour area", areaCnt)
areaRatio = ((areaHull - areaCnt)/areaCnt) * 100 
print("Ratio", areaRatio)
