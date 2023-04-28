import pygame
import socket
import struct
import math
import time
import mapper

TCP_IP_1 = "192.168.0.136"
TCP_IP_2 = "192.168.0.136"
TCP_PORT = 12345

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()



while True:
    try:
        print('connecting to servers...')
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock1.connect((TCP_IP_1, TCP_PORT))
        # sock2.connect((TCP_IP_2, TCP_PORT))
        print('connected.')

        def send_event(event):
            t, a, v = event
            packed_data = struct.pack('!BBH', t, 0xFF & a, 0xFFFF & math.floor(v))
            sock1.sendall(packed_data)
            # sock2.sendall(packed_data)

        while True:
            for event in pygame.event.get():
                vjoy_event = mapper.map_event(event)

                if vjoy_event != None:
                    send_event(vjoy_event)

    except Exception as e:
        print(e)
        sock1.close()
        # sock2.close()
        print('could not connect to all servers, retrying in 1 seconds...')
    time.sleep(1)