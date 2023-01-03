# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 04:23:37 2022

@author: usern
"""

import cv2

vid0 = cv2.VideoCapture(1)
vid1 = cv2.VideoCapture(0)
while (True):
    ret, frame = vid0.read()
    ret2, frame2 = vid1.read()
    cv2.imshow('Frame', frame)
    cv2.imshow('Frame2', frame2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
vid0.release()
vid1.release()
cv2.destroyAllWindows()