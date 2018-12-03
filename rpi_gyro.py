'''
    Read Gyro and Accelerometer by Interfacing Raspberry Pi with MPU6050 using Python
	http://www.electronicwings.com
'''
import smbus			#import SMBus module of I2C
from time import sleep          #import
import struct
import socket
import signal
import sys
import threading, Queue
import traceback

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value


class Telemetrics():
	"""docstring for Telemetrics """
	def __init__(self, arg):
		self.conn = socket.socket()
		host = '192.168.0.101' #ip of raspberry pi
		port = 12355
		self.conn.bind((host, port))
		self.arg = arg
	def SendData(self, gyroData):
		Ax, Ay, Az, Gx, Gy, Gz =  gyroData;
		data_packed = struct.pack('!dddddd', Ax, Ay, Az, Gx, Gy, Gz);
		self.conn.sendall(data_packed)

	def CloseConnection(self):
		self.conn.close()
	def AcceptConnection(self):
		self.conn.listen(5)
		c, addr = self.conn.accept()
		print ('Got connection from', addr)

def MainLoop (queue, telemetrics):
	#c.send('Thank you for connecting')
	# for i in range(100):
	print("Starting the gyro thread");
	while True:
		if not queue.empty():
			stop = queue.get()
			break;
		#Read Accelerometer raw value
		acc_x = read_raw_data(ACCEL_XOUT_H)
		acc_y = read_raw_data(ACCEL_YOUT_H)
		acc_z = read_raw_data(ACCEL_ZOUT_H)
		
		#Read Gyroscope raw value
		gyro_x = read_raw_data(GYRO_XOUT_H)
		gyro_y = read_raw_data(GYRO_YOUT_H)
		gyro_z = read_raw_data(GYRO_ZOUT_H)
		
		#Full scale range +/- 250 degree/C as per sensitivity scale factor
		Ax = acc_x/16384.0
		Ay = acc_y/16384.0
		Az = acc_z/16384.0
		
		Gx = gyro_x/131.0
		Gy = gyro_y/131.0
		Gz = gyro_z/131.0
		
		gyroData = [Ax, Ay, Az, Gx, Gy, Gz];

		print ("Gx=%.2f" %Gx, "Gy=%.2f" %Gy, "Gz=%.2f" %Gz, "Ax=%.2f g" %Ax, "Ay=%.2f g" %Ay, "Az=%.2f g" %Az);
		try:
			telemetrics.SendData(gyroData)
		except Exception, err:
		    traceback.print_exc()
		    break;
	print("Stopping gyro thread.");

class GyroThread():

	"""docstring for GyroThread"""
	def __init__(self, doStreamData):
		self.doStreamData = doStreamData;
		self.isRunning = False;
		self.queue = Queue.Queue()
		self.telemetrics = Telemetrics(None);
		print("Waiting to accept connection.")
		self.telemetrics.AcceptConnection();


	def Start(self):
		print("Starting gyro thread");
		if self.isRunning == False:
			self.thread = threading.Thread(target = MainLoop,
				args = (self.queue, self.telemetrics,)
				).start();
			self.isRunning = True;

	def Stop(self):
		print("Stopping gyro thread");
		if self.isRunning == True:
			stop = True;
			self.queue.put(stop);
		# self.thread.join();


if __name__ =='__main__' :
	bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
	Device_Address = 0x68   # MPU6050 device address

	MPU_Init()

	print (" Reading Data of Gyroscope and Accelerometer")

	gyroThread = GyroThread(True);
	gyroThread.Start();

	sleep(5);

	gyroThread.Stop();

	# threading.Thread(target=MainLoop).start();

	# while  True :
	# 	inp = raw_input("Enter: ");
	# 	if inp == 'x':
	# 		print("Exiting !!")
	# 		break;

	# run = False;
