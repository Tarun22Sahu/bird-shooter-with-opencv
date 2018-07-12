import numpy as np
import cv2
import time
import os
import pyautogui
w=1400
h=770
my_camera = cv2.VideoCapture(0)
my_camera.set(3,w)
my_camera.set(4,h)
time.sleep(2)
while (True):
    success, image = my_camera.read()
    #image = cv2.flip(image,-1)
    image = cv2.GaussianBlur(image,(5,5),0)
    image_HSV = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    lower_pink = np.array([0,150,150])
    upper_pink = np.array([10,255,255])
    mask = cv2.inRange(image_HSV,lower_pink,upper_pink)
    mask = cv2.GaussianBlur(mask,(5,5),0)
    #cv2.imshow('hsv',mask)
    #image = cv2.GaussianBlur(image,(5,5),0)
    #image_HSV1 = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    lower_green = np.array([45,100,100])
    upper_green = np.array([75,255,255])
    mask1 = cv2.inRange(image_HSV,lower_green,upper_green)
    mask1 = cv2.GaussianBlur(mask1,(5,5),0)
    #cv2.imshow('hsv',mask1)
    # findContours returns a list of the outlines of the white shapes in the       mask (and a heirarchy that we shall ignore)
    #print (cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE))
    hierarchy,contours,kl =        cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    hierarchy1,contours1,kl1 =        cv2.findContours(mask1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # If we have at least one contour, look through each one and pick the biggest
    if (len(contours)>0):
        largest = 0
        area = 0
        for i in range(len(contours)):
	    # get the area of the ith contour
            temp_area = cv2.contourArea(contours[i])
            # if it is the biggest we have seen, keep it
            if (temp_area > area):
                area = temp_area
                largest = i
        # Compute the coordinates of the center of the largest contour
        coordinates = cv2.moments(contours[largest])
        target_x = 1372-int(coordinates['m10']/coordinates['m00'])
        target_y = int(coordinates['m01']/coordinates['m00'])
        # Pick a suitable diameter for our target (grows with the contour)
        diam = int(np.sqrt(area)/4)
        # draw on a target
        pyautogui.moveTo(target_x,target_y)
        if (len(contours1)>0):
        	pyautogui.click(target_x,target_y)
        

    #cv2.imshow('View',image)
    # Esc key to stop, otherwise repeat after 3 milliseconds
    key_pressed = cv2.waitKey(3)
    if (key_pressed == 27): 
        break
cv2.destroyAllWindows()
my_camera.release()
# due to a bug in openCV you need to call wantKey three times to get the window to dissappear properly. Each wait only last 10 milliseconds
cv2.waitKey(10)
time.sleep(0.1)
cv2.waitKey(10)
cv2.waitKey(10)
