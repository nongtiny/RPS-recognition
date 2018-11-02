import numpy as np
import cv2
import os

#variables
cap = cv2.VideoCapture(0)
img_counter = 1
path = 'C:\\Users\\Administrator\\RPS\\dataset\\'


kernel = np.ones((3, 3))/9

while(True):
    ret, frame = cap.read()
    #Draw box to detect left side
    cv2.rectangle(frame, (0,100), (300,400), (0,255,0), 0)

    #Draw box to detect right side
    cv2.rectangle(frame, (301,100), (640,400), (0,0,255), 0)

    # Display the resulting frame
    cv2.imshow('frame',frame )

    roi = frame[100:400 , 0:300] #Interest left box area
    roi2 = frame[100:400 , 301:640] #Interest right box area

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

    
    # convert the image into binary image
    # img = roi
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)

    # img2 = roi2
    # gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # blur2 = cv2.GaussianBlur(gray2, (5, 5), 0)
    # ret2, thresh2 = cv2.threshold(blur2, 60, 255, cv2.THRESH_BINARY)
    
    cv2.imshow('left', mask)
    cv2.imshow('right', mask2)
        
    
    k = cv2.waitKey(1)
    if k == 27:  # press ESC to exit
        break
    elif k == ord('b'):  # press 'b' to refresh the background
        bgModel = cv2.createBackgroundSubtractorMOG2(0, 50)
        print( '!!!Background Refreshed!!!')
        
    elif k == ord('s'):    
        img_name = "scis{}.png".format(img_counter)
        cv2.imwrite(os.path.join(path+'train\\scissor', img_name), mask)
        print("{} written!".format(img_name))
        img_counter+=1
    elif k == ord('r'):    
        img_name = "rock{}.png".format(img_counter)
        cv2.imwrite(os.path.join(path+'train\\rock', img_name), mask)
        print("{} written!".format(img_name))
        img_counter+=1
    elif k == ord('p'):    
        img_name = "paper{}.png".format(img_counter)
        cv2.imwrite(os.path.join(path+'train\\paper', img_name), mask)
        print("{} written!".format(img_name))
        img_counter+=1

    elif k & 0xFF == ord('['):
        img_name = "testResultLeft.png"
        cv2.imwrite(os.path.join('C:\\Users\\Administrator\\RPS\\', img_name), mask)
        print("{} written!".format(img_name))
    elif k & 0xFF == ord(']'):
        img_name = "testResultRight.png"
        cv2.imwrite(os.path.join('C:\\Users\\Administrator\\RPS\\', img_name), mask2)  
        print("{} written!".format(img_name))  
   
        
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
