# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 03:42:50 2021

@author: usern
"""
import socket


byte_message = bytes("['z', 100, 200]", "utf-8")
opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
opened_socket.sendto(byte_message, ("192.168.15.197", 4210))