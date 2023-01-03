# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 05:08:22 2021

@author: usern
"""

import cv2
import numpy as np

vid0 = cv2.VideoCapture("http://192.168.15.248:8080/video")
while (vid0.isOpened()==True):
    ret, frame = vid0.read()
    if ret == True:
        print(ret)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    vid0.release()
    cv2.destroyAllWindows()