# Name: Kevan O'Brien
# Email: kobrie32@nd.edu
# File: kobrie32_server.py
#
# Description: Client side script for raspberry pi being used for edge computing

# SERVER: mlab_edge003
# CLIENT: labpi001

import socket
from time import sleep
from time import time

# Establish host and port
host = '10.7.162.80'
port = 8891

# Function to establish socket
def setupSocket():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    return s

# Creat socket for main code
s = setupSocket()
    
reply = s.recv(1024)

print(reply.decode('utf-8'))

s.close()

