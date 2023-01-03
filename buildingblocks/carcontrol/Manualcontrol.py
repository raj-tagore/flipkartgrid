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

    def send_command(self, arr):
        byte_message = bytes(str(arr), " utf-8")
        opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        opened_socket.sendto(byte_message, (self.ip, 4210))


if __name__ == '__main__':

    pg.init()
    Screen01 = pg.display.set_mode((800, 600))
    pg.display.set_caption("botcontrol")

    bot_red = bot()

    speed = 150

    # 1 is wright and 2 is left
    control = ['z', 0, 0]


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


    Running = True
    while Running:
        for event in pg.event.get():
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
