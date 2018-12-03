# DronePi
Git repo with code for Drone project.

How to run:
1. The rpi_server.py runs on the RPi board, reading the MPU6050 data.
2. The rpi_client.py connects to the server and listens for data streams from the server.


This needs to be set to the Client IP
export RPI=192.168.0.100
This needs to be set to the Host IP
export CLIENT=192.168.0.104


scp rpi_server.py pi@$RPI