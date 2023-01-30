import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets

class settings(QWidget):
    def __init__(self):
        super().__init__()
        
        self.labels = [
            ["Save logs","checkbox","save-logs"],
            ["Test","qlineedit","test-setting"]
        ]

        self.control_objects = [] # this saves pointers to checkboxes, qlineedits, etc
        self.label_objects = [] # this saves pointers to labels

        pass
    
    def layout(self):
        
        for x in self.labels:
            self.control_objects.append(QCheckBox()) if x[1] == "checkbox" else False
            self.control_objects.append(QLineEdit()) if x[1] == "qlineedit" else False
                
            self.label_objects.append(QLabel(x[0]))
        
        self.control_objects[0].stateChanged.connect(lambda:self.save_logs(self.control_objects[0]))

        self.horizontal_rows = [QHBoxLayout() for x in range(len(self.control_objects))] # QHbox layouts
        for c,x in enumerate(self.horizontal_rows):
            x.addWidget(self.label_objects[c],1)
            x.addWidget(self.control_objects[c],2)

        self.horizontal_widgets = [QWidget() for x in range(len(self.control_objects))]
        [self.horizontal_widgets[c].setLayout(x) for c,x in enumerate(self.horizontal_rows)]

        self.vertical_stack = QVBoxLayout()
        self.vertical_stack.setAlignment(QtCore.Qt.AlignTop)
        [self.vertical_stack.addWidget(x) for x in self.horizontal_widgets]
        self.vertical_widget = QWidget()
        self.vertical_widget.setLayout(self.vertical_stack)

        self.read_settings()
        if self.settings_numerated[0] == 1:
            self.control_objects[0].setChecked(True)
        
        return self.vertical_widget

    def save_logs(self,b):
        if b.isChecked():
            self.settings_numerated[0] = 1
        else:
            self.settings_numerated[0] = 0
        self.write_settings()
        

    def read_settings(self):
        with open(os.path.join(os.getcwd(), "tab_objects", "settings.txt"), "r") as f:
            self.all_lines = f.readlines()
            self.settings_numerated = []
            for x in self.all_lines:
                self.settings_numerated.append(int(x.replace("\n","").split(" ")[1]))

    def write_settings(self):
        with open(os.path.join(os.getcwd(), "tab_objects", "settings.txt"), "w") as w:
            for c,x in enumerate(self.settings_numerated):
                w.write(f"{self.labels[c][2]}: {x}\n")