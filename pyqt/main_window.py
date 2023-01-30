import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from camera_test import App
from tab_objects.settings import settings
from tab_objects.main_menu import menu


class mainObj(QWidget):
    send_parent_data = QtCore.pyqtSignal(str)

    def __init__(self):
        pass
    
    def layout(self):
        self.tab_layout = QTabWidget()

        #TAB 1
        self.m = menu()
        self.main_menu = self.m.layout()

        #TAB 2
        self.camera_tab_layout = QVBoxLayout()
        self.camera = App()
        self.camera_tab_layout.addWidget(self.camera, 5)
        self.run_button = QPushButton("Take Picture")
        self.run_button.clicked.connect(self.camera.thread.take_image)
        self.camera_tab_layout.addWidget(self.run_button, 1)
        self.result_bar = QTextEdit()
        self.result_bar.setReadOnly(True)
        #self.camera_tab_layout.addWidget(self.result_bar, 1)
        self.start_trip = QPushButton("Start Trip")
        self.start_trip.clicked.connect(self.camera.thread.trip_state)
        self.camera_tab_layout.addWidget(self.start_trip, 1)

        self.camera_tab = QWidget()
        self.camera_tab.setLayout(self.camera_tab_layout)
        


        #TAB 3
        self.settings = settings()
        self.settings_layout = self.settings.layout()
        
        self.tab_layout.addTab(self.camera_tab, "Camera")
        #self.tab_layout.addTab(self.main_menu, "Main Menu")
        self.tab_layout.addTab(self.settings_layout, "Settings")
        
        self.guarddrive_label = QLabel("GuardDrive")
        self.guarddrive_label.setFont(QtGui.QFont("Arial", 20))
        self.guarddrive_label.setAlignment(QtCore.Qt.AlignCenter)

        self.final_qv_tab_layout = QVBoxLayout()
        self.final_qv_tab_layout.addWidget(self.guarddrive_label)
        self.final_qv_tab_layout.addWidget(self.tab_layout)

        self.w = QWidget()
        self.w.setLayout(self.final_qv_tab_layout)
        
        return self.w