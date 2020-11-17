# Name: Kevan O'Brien
# Email: kobrie32@nd.edu
# File: controlPanel.py
#
# Description: Server side script for raspberry pi being used for edge computing

# SERVER: mlab_edge003
# CLIENT: labpi001

from PyQt5.QtWidgets import QApplication, QWidget, QStyle, QStyleFactory, QLabel, QTextEdit, QPushButton, QRadioButton, QMessageBox, QProgressBar, QGridLayout, QVBoxLayout, QGroupBox
from PyQt5.QtCore import Qt
import sys
import socket
import logging
from datetime import datetime
import psutil
import time
import threading
import boto3

# Class for GUI
class Window(QWidget):

    # Initialization / Constructor
    def __init__ (self, parent = None):

        super(Window, self).__init__(parent)

        grid = QGridLayout()

        grid.addWidget(self.createDeviceGroup(), 0, 0)
        grid.addWidget(self.createLogGroup(), 1, 0)
        grid.addWidget(self.createAWSGroup(), 0, 1)
        grid.addWidget(self.createEmptyGroup(), 1, 1)

        self.setLayout(grid)

        self.setWindowTitle('Control Panel')
        self.resize(800, 600)
    
    # Function to create the box to select devices
    def createDeviceGroup(self):

        groupBox = QGroupBox("Select Devices")

        dev1 = QRadioButton('mlab_edge000')
        dev2 = QRadioButton('mlab_edge001')
        dev3 = QRadioButton('mlab_edge002')
        dev4 = QRadioButton('mlab_edge003')

        dev1.setChecked(True)

        box = QVBoxLayout()
        box.addWidget(dev1)
        box.addWidget(dev2)
        box.addWidget(dev3)
        box.addWidget(dev4)
        box.addStretch(1)
        groupBox.setLayout(box)

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
        conn.close()
        
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

# Create GUI
app = QApplication(sys.argv)
window = Window()

t1 = threading.Thread(target = window.show, name = "t1")
#t2 = threading.Thread(target = window.logFile, name = "t2")
t1.start()
#t2.start()
app.exec_()