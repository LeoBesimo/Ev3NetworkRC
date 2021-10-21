#!/usr/bin/env python3

import threading
import os
import socket

from ev3dev2.motor import MoveTank, LargeMotor, OUTPUT_C, OUTPUT_B

os.system('setfont Lat15-TerminusBold14')

serverIp ='192.168.1.28'
port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((serverIp,port))

mt = MoveTank(OUTPUT_C,OUTPUT_B)

def recieve():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            #print(message, "\n")
            temp = message.split(" ")
            #print(float(temp[0].split(":")[1]))
            lSpeed = float(temp[1].split(":")[1])
            rSpeed = float(temp[0].split(":")[1])

            if not rSpeed == 0 or not lSpeed == 0:
                mt.on(left_speed=lSpeed,right_speed=rSpeed)
            else:
                mt.off()

        except:
            pass

recieve()
