import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUiType

form_class = loadUiType("tempd.ui")[0]

class MyWindowClass(QMainWindow, form_class):
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.c2f_button.clicked.connect(self.C2F_clicked)
        self.f2c_button.clicked.connect(self.F2C_clicked)
    def C2F_clicked(self):
        cel=float(self.tmp_textEdit1.toPlainText())
        fahr=cel*9/5.0+32
        self.tmp_textEdit2.setText(str(fahr))
    def F2C_clicked(self):
        fahr=float(self.tmp_textEdit1.toPlainText())
        cel=(fahr-32)/9.0*5
        self.tmp_textEdit2.setText(str(cel))
        
app=QApplication(sys.argv)
myWindow=MyWindowClass(None)
myWindow.show()
app.exec_()


