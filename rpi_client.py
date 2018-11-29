import socket
import struct            

s = socket.socket()        

host = '192.168.0.106'# ip of raspberry pi 
port = 12344
s.connect((host, port))
while True:
	data = s.recv(48);
	if len(data) == 0:
	 	break;
	Ax, Ay, Az, Gx, Gy, Gz = struct.unpack('!dddddd', data);
	print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az)

s.close()