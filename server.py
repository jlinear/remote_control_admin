import socket


host = ''
port = 8891
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

print("Server listening....")

while True:
    conn, addr = s.accept()
    print("Got connection from ", addr)
    data = conn.recv(1024)
    print("Server received", repr(data))
    
    filename = input("Enter filename: ")
    f = open(filename, 'rb')
    l = f.read(1024)
    while(l):
        conn.send(l)
        l = f.read(1024)
    f.close()
    
    print("Done sending")
    conn.close()
    
    