# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 19:31:42 2021

@author: usern
"""

import webbrowser
import urllib.request

speed = 150


webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application/chrome.exe"))

# 1 is wright and 2 is left
control = ['z',0,0]
print(control) 
def forward():
    control[2] = -speed
    control[1] = speed
def backward():
    control[2] = speed
    control[1] = -speed
def right():
    control[2] = -speed
    control[1] = -speed
def left():
    control[2] = speed
    control[1] = speed
def stop():
    control[2] = 0
    control[1] = 0
    
def sendrequest(arr):
    try:
        #webbrowser.get('chrome').open("http://192.168.15.114/"+str(arr))
        # 192.168.15.100


        arr = str(arr).replace(" ", "")
        urllib.request.urlopen("http://192.168.15.100/"+arr)
    except ConnectionError:
        print("sent")
        

while True:
    key = input();
    if key=='w':
        forward()
        sendrequest(control)
    elif key == 's':
        backward()
        sendrequest(control)    
    elif key=='a':
        left()
        sendrequest(control)
    elif key=='d':
        right()
        sendrequest(control)
    elif key=='x':
        stop()
        sendrequest(control)
    else:
        control[0] = 'x'
        sendrequest(control)
        break

