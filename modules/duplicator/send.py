import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'shared')))

import pygame
import socket
import math
import time
import ds_utils

TCP_IP_1 = "192.168.0.136"
TCP_PORT = 12345

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

while True:
    try:
        print('connecting to servers...')
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock1.connect((TCP_IP_1, TCP_PORT))
        print('connected.')

        while True:
            for event in pygame.event.get():
                vjoy_event = ds_utils.event_pygame2vjoy(event)
                if vjoy_event != None:
                    sock1.send(ds_utils.encode_vjoy_event(vjoy_event))
    except Exception as e:
        print(e)
        sock1.close()
        # sock2.close()
        print('could not connect to all servers, retrying in 1 seconds...')
    time.sleep(1)