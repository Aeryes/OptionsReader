#gui.py

#Imports
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QLabel,
    QMainWindow,
    QStackedWidget,
    QHBoxLayout,
)
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon 

import os
import sys

class GUIObject(QWidget):
	def __init__(self):
		super(GUIObject, self).__init__()
		self.setWindowTitle("OptionsReader")

        #Child widgets.
		self.startWidget = QWidget()
		self.doneWidget = QWidget()

		#Initialize the layouts.
		self.setStartLayout()
		self.setDoneLayout()

		#Create the Stack add children to the stack.
		self.Stack = QStackedWidget(self)
		self.Stack.addWidget(self.startWidget)
		self.Stack.addWidget(self.doneWidget)

		#Create the outer container.
		hbox = QHBoxLayout(self)
		hbox.addWidget(self.Stack)
       
		self.setLayout(hbox)
		self.setGeometry(300, 50, 1200,500)
		self.show()

	def setStartLayout(self):
        #################
        #LAYOUT OPTION 1#
        #################

        #Labels for layout option 1
		self.introLabel = QLabel("Hit the start button to begin the data processing...")

		#Buttons for layout 1
		self.startButton = QPushButton("Start")
		#self.startButton.clicked.connect(self.selectLayoutDone())
        
        #Outer Layout for the nested layout style.
		self.outerLayoutAppStart = QVBoxLayout()

        #Create QLabel for text display.
		self.topLayout = QVBoxLayout()
		self.introLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.topLayout.addWidget(self.introLabel)

		# Create a QGridLayout instance
		self.bottomLayout = QGridLayout()
		self.bottomLayout.addWidget(self.startButton, 0, 0, 1, 2)

		#Add layouts to the outer layout.
		self.outerLayoutAppStart.addLayout(self.topLayout)
		self.outerLayoutAppStart.addLayout(self.bottomLayout)

		# Set the initial layout on the application's window
		self.startWidget.setLayout(self.outerLayoutAppStart)
		#self.setCentralWidget(self.startWidget)

	def setDoneLayout(self):
		#################
		#LAYOUT OPTION 2#
		#################

		#Labels for layout option 2.
		self.percentDoneLabel = QLabel()
		self.resultLabel = QLabel()

		# #Buttons for layout 2
		self.doneButton = QPushButton("Done")
		#self.doneButton.clicked.connect(self.selectLayoutStart(1))

		#Outer Layout for the nested layout style.
		self.outerLayoutAppResults = QVBoxLayout()

        #Create QLabel for text display.
		self.topLayoutTwo = QVBoxLayout()
		self.introLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.topLayoutTwo.addWidget(self.percentDoneLabel)
		self.topLayoutTwo.addWidget(self.resultLabel)

		# Create a QGridLayout instance
		self.bottomLayoutTwo = QGridLayout()
		self.bottomLayoutTwo.addWidget(self.doneButton, 0, 0, 1, 2)

		#Add layouts to the outer layout.
		self.outerLayoutAppResults.addLayout(self.topLayoutTwo)
		self.outerLayoutAppResults.addLayout(self.bottomLayoutTwo)	

		self.doneWidget.setLayout(self.outerLayoutAppResults)			

	def display(self, index):
		self.Stack.setCurrentIndex(index)
		