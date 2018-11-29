#!/usr/bin/env python3

import socket

HOST = '192.168.0.104'  # The server's hostname or IP address
PORT = 65433        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	while True:
		#data = s.recv(1024)
		s.sendall(b'Hello, world')
		#print('Received', repr(data))
		# if data == b'':
		# 	break;
s.close()