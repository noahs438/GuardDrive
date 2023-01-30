import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets
from main_window import mainObj

class final(QMainWindow):
    def __init__(self):
        super().__init__()
        self.f = mainObj()
        self.hl = self.f.layout()

        self.resize(700, 700)

        self.setCentralWidget(self.hl)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = final()
    mw.show()
    mw.setWindowTitle("GuardDrive")
    sys.exit(app.exec_())