# Name: Kevan O'Brien
# Email: kobrie32@nd.edu
# File: controlPanel.py
#
# Description: Server side script for raspberry pi being used for edge computing

# SERVER: mlab_edge003
# CLIENT: labpi001

from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QStyle, QStyleFactory, QLabel, QTextEdit, QPushButton, QRadioButton, QMessageBox, QProgressBar, QGridLayout, QVBoxLayout, QGroupBox
from PyQt5.QtCore import Qt
import sys
import socket
import logging
from datetime import datetime
import psutil
import time
import threading
import boto3
import os

# Class for GUI
class Window(QWidget):

    # Initialization / Constructor
    def __init__ (self, parent = None):

        super(Window, self).__init__(parent)

        grid = QGridLayout()

        grid.addWidget(self.createLogGroup(), 1, 0)
        grid.addWidget(self.createAWSGroup(), 0, 1)
        grid.addWidget(self.createFtpGroup(), 1, 1)
        grid.addWidget(self.createDeviceGroup(), 0, 0)

        self.setLayout(grid)

        self.setWindowTitle('Control Panel')
        self.resize(800, 600)
    
    # Function to create the box to select devices
    def createDeviceGroup(self):

        threading.Timer(3.0, self.createDeviceGroup).start()

        groupBox = QGroupBox("Select Devices")
        
        r1 = os.system("ping -c 1 " + "10.7.162.108")
        r2 = os.system("ping -c 1 " + "10.7.111.190")
        r3 = os.system("ping -c 1 " + "10.7.159.211")
        r4 = os.system("ping -c 1 " + "10.7.180.205")
        
        if r1 == 0:
            
            response1 = "Online"
            
        else:
                
            response1 = "Offline"
            
        if r2 == 0:
            
            response2 = "Online"
            
        else:
                
            response2 = "Offline"
            
            
        if r3 == 0:
            
            response3 = "Online"    
            
        else:
                
            response3 = "Offline"            
            
        if r4 == 0:
            
            response4 = "Online"    
            
        else:
                
            response4 = "Offline"      
            

        dev1 = QRadioButton('mlab_edge000 - {}'.format(response1))
        dev2 = QRadioButton('mlab_edge001 - {}'.format(response2))
        dev3 = QRadioButton('mlab_edge002 - {}'.format(response3))
        dev4 = QRadioButton('mlab_edge003 - {}'.format(response4))
        
        box = QVBoxLayout()
        box.addWidget(dev1)
        box.addWidget(dev2)
        box.addWidget(dev3)
        box.addWidget(dev4)
        box.addStretch(1)
        groupBox.setLayout(box)
                
        if dev1.isChecked():
            
            print("Device 1 has been selected")
        
        if dev2.isChecked():
            
            print("Device 2 has been selected")
        
        if dev3.isChecked():
            
            print("Device 3 has been selected")
            
        if dev4.isChecked():
            
            print("Device 4 has been selected")

        return groupBox
    
    def createLogGroup(self):
        
        groupBox = QGroupBox("Logs")
        
        log = QTextEdit()
        log.setReadOnly(True)
        log.setLineWrapMode(QTextEdit.NoWrap)
       
        host = ''
        port = 8891

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(1)

        print("Server listening...")

        conn, addr = s.accept()
        print("Got connection from ", addr)
        output = "Got connection from {}".format(addr)
        
        #send files
        #f = open("test.txt", "rb")
        #f = open("test_pic.jpg", "rb")
        f = open("test.py", "rb")
          
        l = f.read(1024)
        
        while(l):
            
            print("Sending file...")
            conn.send(l)
            l = f.read(1024)
        
        print("Done sending")
        
        conn.close()
        s.close()
        
        log.append(output)
        
        box = QVBoxLayout()
        box.addWidget(log)
        
        box.addStretch(1)    
        groupBox.setLayout(box)
        
        return groupBox        

    # Function to make a box to display log data and create a log file
    def logFile(self):
        
        now = datetime.now()
        curTime = now.strftime("%H:%M:%S")
        
        logging.basicConfig(filename = "CP_Log_{}.log".format(curTime), level = logging.DEBUG)
        logging.info("Start Time: {}".format(curTime))
        
        #while(True):
            
            # ERROR - can't access socket due to scoping
            #logging.info(s.recv)
        
            #time.sleep(3)
    
    # Function to create box to print out incoming AWS data
    def createAWSGroup(self):
        
        groupBox = QGroupBox("AWS Status")
        
        log = QTextEdit()
        log.setReadOnly(True)
        log.setLineWrapMode(QTextEdit.NoWrap)
        
        box = QVBoxLayout()
        box.addWidget(log)
        
        box.addStretch(1)    
        groupBox.setLayout(box)
        
        client = boto3.client("cloudwatch")
                
        # List metrics through the pagination interface
        paginator = client.get_paginator('list_metrics')
        for response in paginator.paginate(Dimensions=[{'Name': 'LogGroupName'}],
                                   MetricName='IncomingLogEvents',
                                   Namespace='AWS/Logs'):
            print(response['Metrics'])
            log.append('Metrics')
            
        client2 = boto3.client("greengrass")
        
        # Get greengrass data
        groupsResponse = client2.list_groups()
        print(groupsResponse)
        log.append(str(groupsResponse))
        
        deploymentsResponse = client2.list_deployments(
         
            GroupId = 'ca72ad0c-7eb2-4ed7-bc0e-dc957a2bacb6'
            
        )       
            
        print(deploymentsResponse)
        log.append(str(deploymentsResponse))
            
        return groupBox    
    
    # Function to create empty box template
    def createEmptyGroup(self):

        groupBox = QGroupBox("Empty")

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox
    
    # Function to create ftp box
    def createFtpGroup(self):
        
        groupBox = QGroupBox("FTP")
        
        selectFile = QPushButton("Select File")
        
        def fileSelect(self):
        
            dlg = QFileDialog()
            dlg.setFileMode(QFileDialog.AnyFile)
            filenames = ''
            
            if dlg.exec_():
               
                filenames = dlg.selectedFiles()
                
            return filenames
                
        box = QVBoxLayout()
        box.addWidget(selectFile)
        selectFile.clicked.connect(fileSelect)
        box.addStretch(1)       
        groupBox.setLayout(box)
        
        return groupBox

# Create GUI
app = QApplication(sys.argv)
window = Window()

t1 = threading.Thread(target = window.show, name = "t1")
#t2 = threading.Thread(target = window.logFile, name = "t2")
t1.start()

#t2.start()
app.exec_()
