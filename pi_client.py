import socket
from struct import * 

str=input("Enter the Direction :  ")
num=int(str)
s = socket.socket()
host = "192.168.43.223"
port = 8001
s.connect((host,port))
print("connection established")
#s.send(val.encode())
val = pack('!i', num)
s.send(val)
