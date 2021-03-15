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
import sys
import logging
from datetime import datetime
import psutil
import time
import threading

# Establish host and port
host = '10.7.180.205'
port = 8891

# Function to establish socket
def setupSocket():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    return s

def logFile():
        
    now = datetime.now()
    curTime = now.strftime("%H:%M:%S")
    
    #while(True):
     
        #cpu = psutil.cpu_percent()
        #memDict = dict(psutil.virtual_memory()._asdict())
        #mem = psutil.virtual_memory().percent
        
        #now = datetime.now()
        #curTime = now.strftime("%H:%M:%S")
        
        # ERROR - error in sending string
        #s.send("Time: {}   CPU Usage: {}%   Memory Usage: {}%".format(curTime, cpu, mem).encode())
    
        #time.sleep(3)

# Creat socket for main code
s = setupSocket()

t1 = threading.Thread(target = logFile, name = "t1")
t1.start()

print("Receiving data...")

f = open("test_copy.txt", 'wb')
while True:
    
    buf = s.recv(1024)
    if buf == "":
        
        break
    
    f.write(buf)
    
print("File received")
f.close()

print(reply.decode('utf-8'))

s.close()
