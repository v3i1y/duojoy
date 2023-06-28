import socket
import struct
import os
import pyvjoy
import time
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'shared')))
import ds_utils

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
            while True:
                data = conn.recv(4)
                if data:
                    ds_utils.run_vjoy_event(j, ds_utils.decode_vjoy_event(data))
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