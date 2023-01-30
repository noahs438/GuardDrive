from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import time
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from tab_objects.input_into_model import model_output
from PIL import Image
import io
import datetime
import time

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.count = 0
        self.grab_model = model_output()
        self.result = [0,0]
        self.trip_start = True
        self.trip_not_started_image = Image.open('trip_start.jpg')
        self.numpydata = np.asarray(self.trip_not_started_image)
        self.last_result = ""
        self.streak = 0

    def run(self):
        # capture from web cam
        with open("log.txt", "w") as w:
            self.image_perm = False
            cap = cv2.VideoCapture(0)
            while self._run_flag:
                ret, cv_img = cap.read()
                pil_img = Image.fromarray(np.uint8(cv_img*255))

                # Create a BytesIO object
                img_io = io.BytesIO()

                # Save the PIL image to the BytesIO object
                pil_img.save(img_io, 'JPEG')
                img_io.seek(0)
                #print(f"{type(cv_img)}->{type(img_io)}")
                self.result = self.grab_model.check_image(img_io)
                time.sleep(250/1000)
                self.count = self.count + 1
                if self.last_result == self.result[0]:
                    self.streak = self.streak + 1
                else:
                    self.streak = 1
                self.last_result = self.result[0]
                
                print("{} {} {:.2f} Streak: {}".format(self.count,self.result[0],self.result[1],self.streak))
                w.write("{} {} {:.2f} Streak: {}\n".format(self.count,self.result[0],self.result[1],self.streak))

                #ret is boolean, cv_img is an image object
                if ret:
                    if self.trip_start:
                        self.change_pixmap_signal.emit(cv_img)
                    else:
                        self.change_pixmap_signal.emit(self.numpydata)
                    #cv2.imwrite("test_image.png", cv_img)
                    if self.image_perm:
                        self.image_perm = False
                        cv2.imwrite("test_image.png", cv_img)
                        print("picture taken")
                    
            # shut down capture system
            cap.release()

    def take_image(self):
        self.image_perm = True

    def trip_state(self):
        print("activated")
        if self.trip_start:
            self.trip_start = False
        else:
            self.trip_start = True

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

    def ymd_hms(self):
        """ year-month-day hour:minute:second

        :return: returns a string which is derived from datetime. in the format listed in the summary
        :rtype: str
        """        
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
        return ts




class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 640
        self.display_height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)


        # create a vertical box layout and add the two labels
        

        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        
        # start the thread
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()



    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())