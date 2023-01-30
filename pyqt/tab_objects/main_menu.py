import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets

class menu(QWidget):
    def __init__(self):
        pass

    def layout(self):
        self.main_menu_layout = QVBoxLayout()
        self.main_menu_layout.addWidget(QLabel("Hello World!"))

        self.main_menu = QWidget()
        self.main_menu.setLayout(self.main_menu_layout)

        return self.main_menu