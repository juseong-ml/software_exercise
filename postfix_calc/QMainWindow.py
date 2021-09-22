import sys
from PyQt5.QtWidgets import *

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle("QMainWindow")
        self.setGeometry(300, 300, 300, 400)

app = QApplication(sys.argv)
myWindow = MyWindow()
myWindow.show()
app.exec_()
