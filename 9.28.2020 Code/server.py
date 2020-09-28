# Name: Kevan O'Brien
# Email: kobrie32@nd.edu
# File: kobrie32_server.py
#
# Description: Server side script for raspberry pi being used for edge computing

# SERVER: mlab_edge003
# CLIENT: labpi001

import socket

# Establish host and port
host = ''
port = 8891

# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

print("Server listening...")

# Function to receive remote file and store it locally
def storeFile(filePath):
    
    local = open(filePath, 'wb')
    print("Created local file...")
    remote = conn.recv(1024)
    
    while remote:
        
        print("Receiving file still...")
        local.write(remote)
        remote = conn.recv(1024)
        
    local.close()
    
    print("Finished writing to local file...")

# Main code
conn, addr = s.accept()
print("Got connection from ", addr)
data = conn.recv(1024)
print("Server received", repr(data))

path = input("Path to store file locally: ")

storeFile(path)
    
conn.close()
