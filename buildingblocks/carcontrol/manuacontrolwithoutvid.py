import pygame as pg
import cv2
import numpy as np
import time
import socket


class bot:
    position = []
    angle: int = 0
    destination = []
    path = [58, 9, 6, 55, 58]
    path_equations = [[]]
    next_target = 1
    rms = 0
    lms = 0
    ip = "192.168.15.249"

    # 192.168.15.178 -- 4 spoilt wire
    # 192.168.15.126 -- 5
    # 192.168.15.148



    # 192.168.15.197 - orange
    # 192.168.15.178 - violet
    # 192.168.15.114 - blue
    # 192.168.15.249 - red

    def send_command(self, arr):
        byte_message = bytes(str(arr), "utf-8")
        opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        opened_socket.sendto(byte_message, (str(self.ip), 4210))


if __name__ == '__main__':


    pg.init()
    Screen01 = pg.display.set_mode((200, 200))
    pg.display.set_caption("botcontrol")

    bot_red = bot()

    speed = 220
    angle = 30

    # 1 is wright and 2 is left
    control = [0, 0, 0, 0]


    def forward():
        control[2] = speed
        control[1] = speed
        control[0] = 0
        control[3] = 0


    def backward():
        control[2] = -speed
        control[1] = -speed
        control[0] = 0
        control[3] = 0


    def right():
        control[2] = 0
        control[1] = 0
        control[0] = 0
        control[3] = -angle


    def left():
        control[2] = 0
        control[1] = 0
        control[0] = 0
        control[3] = angle

    def stop():
        control[2] = 0
        control[1] = 0
        control[0] = 0
        control[3] = 0


    def eject():
        control[2] = 0
        control[1] = 0
        control[0] = 1
        control[3] = 0


    Running = True
    while Running:
        for event in pg.event.get():
            t1 = time.time()
            if event.type == pg.QUIT:
                Running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_d:
                    right()
                    bot_red.send_command(control)
                if event.key == pg.K_a:
                    left()
                    bot_red.send_command(control)
                if event.key == pg.K_w:
                    forward()
                    bot_red.send_command(control)
                if event.key == pg.K_s:
                    backward()
                    bot_red.send_command(control)
                if event.key == pg.K_e:
                    eject()
                    bot_red.send_command(control)

            # event where button is let-go
            if event.type == pg.KEYUP:
                stop()
                bot_red.send_command(control)

            print(control)
            t2 = time.time()
            print(t2-t1)
