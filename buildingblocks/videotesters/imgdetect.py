# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 16:36:30 2021

@author: usern
"""

import cv2
import numpy as np

"""vid0 = cv2.VideoCapture("http://192.168.15.248:8080/browserfs.html")
while (vid0.isOpened()==True):
    ret, frame = cap.read()
    if ret == True:
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    vid0.release()
    cv2.destroyAllWindows()"""
    
image = cv2.imread(r"C:\Users\usern\Pictures\Screenshots/Screenshot (47).png")
 
#resize image
scale_percent = 60 # percent of original size
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

#convert to pure B/W
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (13,13), 0)
thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

c = 0
viablecontours = []
for i in contours:
        area = cv2.contourArea(i)
        if area > 1000:
            viablecontours.append(c)
            #cv2.drawContours(image, contours, c, (0, 255, 0), 3)
        c+=1
for i in range(56):
    cv2.drawContours(image, contours, 65+i, (0, 255, 0), 3)
    #cv2.imshow(str(i), image)
    #cv2.waitKey(0)
cv2.imshow("thresh", thresh)
cv2.waitKey(0)    
cv2.imshow("Final Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()