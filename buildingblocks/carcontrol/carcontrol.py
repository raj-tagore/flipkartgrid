import socket

speed = 150

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
def eject():
    control[2] = 0
    control[1] = 0
    control[0] = 'e'
    
def sendrequest(arr):
    try:
        # 192.168.15.249
        # 192.168.15.100
        byte_message = bytes(str(arr), " utf-8")
        opened_socket = socket. socket(socket. AF_INET, socket. SOCK_DGRAM)
        opened_socket. sendto(byte_message, ("192.168.15.197", 4210))
        

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
    elif key == 'e':
        eject()
        sendrequest(control)
    else:
        control[0] = 'x'
        sendrequest(control)
        break

