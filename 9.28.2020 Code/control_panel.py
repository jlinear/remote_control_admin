from PyQt5.QtWidgets import QApplication, QWidget, QStyle, QStyleFactory, QLabel, QPushButton, QRadioButton, QMessageBox, QProgressBar, QGridLayout, QVBoxLayout, QGroupBox
from PyQt5.QtCore import Qt
import sys

class Window(QWidget):

    def __init__ (self, parent = None):

        super(Window, self).__init__(parent)

        grid = QGridLayout()

        grid.addWidget(self.createDeviceGroup(), 0, 0)
        grid.addWidget(self.createEmptyGroup(), 1, 0)
        grid.addWidget(self.createEmptyGroup(), 0, 1)
        grid.addWidget(self.createEmptyGroup(), 1, 1)

        self.setLayout(grid)

        self.setWindowTitle('Control Panel')
        self.resize(800, 600)

    def createDeviceGroup(self):

        groupBox = QGroupBox("Select Devices")

        dev1 = QRadioButton('mlab_edge000')
        dev2 = QRadioButton('mlab_edge001')
        dev3 = QRadioButton('mlab_edge002')
        dev4 = QRadioButton('mlab_edge003')

        dev1.setChecked(True)
		
		if dev1.isChecked():
		
			print("Device 1 has been selected")
			
		if dev2.isChecked():
		
			print("Device 2 has been selected")
			
		if dev3.isChecked():
		
			print("Device 3 has been selected")
			
		if dev4.isChecked():
		
			print("Device 4 has been selected")

        vbox = QVBoxLayout()
        vbox.addWidget(dev1)
        vbox.addWidget(dev2)
        vbox.addWidget(dev3)
        vbox.addWidget(dev4)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createEmptyGroup(self):

        groupBox = QGroupBox("Empty")

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

app = QApplication(sys.argv)
window = Window()
window.show()
app.exec_()
