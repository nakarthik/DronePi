#!/usr/bin/env python3

import socket
import time
import struct

HOST = '192.168.0.106'  # Standard loopback interface address (localhost)
PORT = 12346       # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            print("in loop")
            data = conn.recv(1024)
            if data == b'':
                break;
            #data=b'Hello'n
            #conn.sendall(data);
            # Ax, Ay, Az, Gx, Gy, Gz = struct.unpack('!dddddd',data);
            # print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az)
            print(data)