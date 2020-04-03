import socket
import threading
from time import sleep
from time import time
from queue import Queue

NUM_OF_THREADS = 2
JOB_NUM = [1, 2]
queue = Queue()
all_connections = []
all_address = []

# vars used to print correct prompt after a new connection
# new connections are printed and move cursor to a new line
# global in_shell
# control_switch = 0


def create_socket():
    try:
        global host
        global port
        global s
        host = ''
        port = 8891
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    except socket.error as msg:
        print("Socket creation error: " + str(msg))
        
def bind_socket():
    try:
        global host
        global port
        global s
        
        s.bind((host, port))
        s.listen(1)
        
    except socket.error as msg:
        print("Socket Bindingg error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


def accepting_connection():
    global in_shell
    global control_switch
    # closing previous connection when server.py file is restarted
    for c in all_connections:
        c.close()
        
    del all_connections[:]
    del all_address[:]
    
    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1) # prevents timeout
            
            all_connections.append(conn)
            all_address.append(address)
            
            print("\n" + "Connection has been established: " + address[0])
            print(in_shell)
            if in_shell:
                print("shell> ", end = "", flush = True)
            else:
                if control_switch == 0:
                    print("Enter command: ", end = "", flush = True)
                elif control_switch == 1:
                    print("Enter filename: ", end = "", flush = True)
            
        except:
            print("Error accepting connections")
        

# 2nd thread functions - 1) See all the clients 2) select a client 3) send commands to client
# Interactive prompt for sending commands

def start_shell():
    global in_shell
    
    while True:
        in_shell = True
        cmd = input('shell> ')
        if cmd == 'list':
            list_connections()
        
        elif 'select' in cmd:
            in_shell = False
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("Command not recognized")
        
        
# Display all current active connections with the client
def list_connections():
    print("----Clients----")
    
    for i,conn in enumerate(all_connections):
        # conn.send(str.encode(' '))
        # conn.recv(20480)
        if conn is None:
            del all_connections[i]
            del all_address[i]
            continue
        
        print(str(i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]))
        
    # print("----Clients----" + "\n" + results)
    

# Selecting the target
def get_target(cmd):
   # print("+++++++++++++++++")
    try:
         # print("+++++++++++++++++")
        target = cmd.replace('select ','') # target = id
        target = int(target)
        # print("+++++++++++++++++")
       
        conn = all_connections[target]
        print("You are now connected to: " + str(all_address[target][0]))
        
        
    except:
        print("Selection not valid")
        
    return conn


def send_target_commands(conn):
    global in_shell
    global control_switch
    
    while True:
        in_shell = False
        try:
            cmd = input("Enter command: ")
            if cmd == 'quit':
                in_shell = True
                break
            elif cmd == 'store':
                control_switch = 1
                filename = input("Enter filename: ")
                f = open(filename, 'rb')
                l = f.read(1024)
                t = time()
                while(l):
                    conn.send(l)
                    l = f.read(1024)
                    print("sending...")
                f.close()
                 
                print("Done sending")
                print("Elapsed time = " + str(time() - t) + 's')
                control_switch = 0
                conn.close()
        
        except OSError as err:
            print("OS error: {0}".format(err))
            #print("Error sending commands")
            break
        

# Send picture to client
# def send_pic(conn, filePath):
#     f = open(filePath, 'rb')
#     l = f.read(8192)
#     conn.send(str.encode("STORE " + filePath))
#     t = time()
#     while(l):
#         conn.send(l)
#         l = f.read(8192)
#     f.close()
#     print("Done Sending")
#     print("Elapsed time = " + str(time() - t) + 's')
    
# Create worker threads
def create_workers():
    for _ in range(NUM_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Do next job that is in the queue (handle, connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connection()
        if x == 2:
            start_shell()
            
        queue.task_done()
        
def create_jobs():
    for x in JOB_NUM:
        queue.put(x)
        
    queue.join()


create_workers()
create_jobs()