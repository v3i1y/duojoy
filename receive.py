import socket
import struct
import os
import pyvjoy
import time
import sys

j = pyvjoy.VJoyDevice(1)

print("Connected to virtual gamepad.")

TCP_IP = "0.0.0.0"
TCP_PORT = 12345
BUFFER_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(1)
sock.settimeout(0.5)

print("Start listening for incoming connection...")
while True:
    try:
        try:
            conn, addr = sock.accept()
            print("Connected to " + str(addr))

            sock.settimeout(0.5)
            VJOY_POV_UP = 0
            VJOY_POV_RIGHT = 2

            VJOY_INPUT_TYPE_BUTTON = 0
            VJOY_INPUT_TYPE_AXIS   = 1
            VJOY_INPUT_TYPE_POV    = 2

            while True:
                data = conn.recv(4)

                if data:
                    event_type, axis, value = struct.unpack('!BBH', data)
                    if event_type == VJOY_INPUT_TYPE_BUTTON:
                        j.set_button(axis, True if value == 1 else False)
                    if event_type == VJOY_INPUT_TYPE_POV:
                        j.set_cont_pov(1, axis * 10000 if value == 1 else -1)
                    if event_type == VJOY_INPUT_TYPE_AXIS:
                        j.set_axis(axis, value)
                else:
                    print("Connection from " + str(addr) + " closed...")
                    break
        except socket.timeout:
            pass
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit()
    except Exception as e:
        print("Connection interrupted...")
        print(e)