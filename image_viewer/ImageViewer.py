import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, qApp, QFileDialog, QWidget, QRubberBand
from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.uic import loadUiType
from PyQt5.QtGui import *
import os
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
import blur

form_class1 = loadUiType("imageViewer.ui")[0]
form_class2 = loadUiType("dialog.ui")[0]

class AnotherWindow(QWidget,form_class2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class ViewerClass(QMainWindow, form_class1):
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.qPixmapVar = QPixmap()
        self.actionFile_Select.triggered.connect(self.fileSelect)
        self.actionto_Gray.triggered.connect(self.toGraySelect)
        self.actionCrop.triggered.connect(self.imageCrop)
        self.actionFolder_Select.triggered.connect(self.folderSelect)
        self.actionNext.triggered.connect(self.moveNextClick)
        self.actionMedian.triggered.connect(self.blur_median)
        self.actionGaussian.triggered.connect(self.blur_gaussian)
        self.actionEast.triggered.connect(self.shift_east)
        self.actionWest.triggered.connect(self.shift_west)
        self.actionSouth.triggered.connect(self.shift_south)
        self.actionNorth.triggered.connect(self.shift_north)
        self.actionRotate.triggered.connect(self.show_new_window)
        self.actionExit.triggered.connect(qApp.quit)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        self.idx = 0
        self.hh = 600
        self.ww = 600
        self.cropEnable = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.origin = QPoint(event.pos())
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()

    def mouseMoveEvent(self, event):
        if not self.origin.isNull():
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.rubberBand.hide()
        if self.cropEnable == True:
            self.selStart = self.origin - self.startPos - QPoint(0, 20) # 선택된 좌측 상단 좌표
            self.selEnd = event.pos() - self.startPos - QPoint(0, 20)   # 선택된 우측 하단 좌표
            print(self.selStart, self.selEnd)
            print(self.selStart.x() / self.img_width_tran, self.selStart.y() / self.img_height_tran)
            print(self.selEnd.x() / self.img_width_tran, self.selEnd.y() / self.img_height_tran)
            cut_begin_x = int(self.img_width_origin * self.selStart.x() / self.img_width_tran)
            cut_begin_y = int(self.img_height_origin * self.selStart.y() / self.img_height_tran)
            cut_end_x = int(self.img_width_origin * self.selEnd.x() / self.img_width_tran)
            cut_end_y = int(self.img_height_origin * self.selEnd.y() / self.img_height_tran)
            self.img = self.img[cut_begin_y:cut_end_y, cut_begin_x:cut_end_x,:].astype('uint8')
            self.img2label(self.img)
            self.cropEnable = False

    def img2label(self, img):
        self.qPixmapVar = QPixmap(self.img2QImage(img))
        self.qPixmapVar = self.qPixmapVar.scaled(self.hh, self.ww, aspectRatioMode=True)
        self.label.setPixmap(self.qPixmapVar)

    def fileSelect(self):
        self.fName = QFileDialog.getOpenFileName(self, 'Open file', 'D:/NaverCloud/lecture/pywork/swexer2020/images',"Image files (*.jpg)")[0]
        self.img = cv2.imread(self.fName)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.img_height_origin = self.img.shape[0]
        self.img_width_origin = self.img.shape[1]
        print(self.img.shape)
        self.img2label(self.img)

    def imageCrop(self):
        self.cropEnable = True
        self.hw_ratio = self.img_height_origin / self.img_width_origin  # > 1 이면 세로 사진, < 1 은 가로 사진
        print(self.img_height_origin, self.img_width_origin)

        if self.hw_ratio > 1:  # 세로사진이면 높이를 최대 길이가 되고 너비는 비례로 작아진다.
            self.img_height_tran = self.hh
            self.img_width_tran = int(self.img_height_tran / self.img_height_origin * self.img_width_origin)
        else:
            self.img_width_tran = self.ww  # 가로 사진이면 너비를 최대로 하고 높이를 비례로 조정한다.
            self.img_height_tran = int(self.img_width_tran / self.img_width_origin * self.img_height_origin)
        print(self.img_height_tran, self.img_width_tran)

        if self.img_width_tran < self.ww:    # 너비가 축소되었다면
            self.startPos = QPoint((self.ww - self.img_width_tran) // 2, 0)        # (600,600) 중 화면에 보이는 이미지 좌측 상단 좌표
            self.endPos = QPoint(self.startPos.x() + self.img_width_tran, self.hh) # (600,600) 중 화면에 보이는 이미지 우측 하단 좌표
        else:                                # 높이가 축소되었다면
            self.startPos = QPoint(0, (self.hh - self.img_height_tran) // 2)
            self.endPos = QPoint(self.ww, self.startPos.y() + self.img_height_tran)
        print(self.startPos, self.endPos)

    def show_new_window(self):
        self.w = AnotherWindow()
        self.w.horizontalSlider.valueChanged.connect(self.rotate_image)
        self.w.show()

    def rotate_image(self):
        angle = self.w.horizontalSlider.value()
        print("%d 도로 회전합니다" % angle)
        # rad = np.pi / (180 / angle)
        # x0 = self.img_height_origin // 2  # 이미지의 중심좌표를 구한다.
        # y0 = self.img_width_origin // 2
        #
        # newImg = np.zeros((self.img_height_origin, self.img_width_origin, 3)).astype('uint8')  # 빈 이미지를 만든다.
        #
        # for k in range(3):
        #     for i in range(self.img_height_origin):
        #         for j in range(self.img_width_origin):
        #             # 이미지의 모든 i, j에 대해 중심을 원점으로 rad 만큼 회전한 좌표를 구한다.
        #             x = int((i - x0) * np.cos(rad) - (j - y0) * np.sin(rad) + x0)
        #             y = int((i - x0) * np.sin(rad) + (j - y0) * np.cos(rad) + y0)
        #             # 해당 좌표가 이미지 공간을 벗어나지 않으면 회전된 위치에 값을 복사한다.
        #             if (x < self.img_height_origin) and (x >= 0):
        #                 if (y < self.img_width_origin) and (y >= 0):
        #                     newImg[x, y, k] = self.img[i, j, k]
        blurImg = blur.angle_rotate(self.img, h=self.img_height_origin, w=self.img_width_origin, angle=angle)
        blurImg = np.require(blurImg, np.uint8, 'C')
        self.img2label(blurImg)

    def toGraySelect(self):
        r_img = self.img[:, :, 0]
        g_img = self.img[:, :, 1]
        b_img = self.img[:, :, 2]
        imgGray = 0.21 * r_img + 0.72 * g_img + 0.07 * b_img
        self.img[:, :, 0] = imgGray
        self.img[:, :, 1] = imgGray
        self.img[:, :, 2] = imgGray
        self.img2label(self.img)

    def medFilter(self, img):
        return np.median(img)

    def blur_median(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        # img_median = self.img[:,:,:]
        # for k in range(3):
        #     for i in range(1, self.img_height_origin-1):
        #         for j in range(1, self.img_width_origin-1):
        #             med = self.medFilter(self.img[i - 1:i + 2, j - 1:j + 2, k])
        #             img_median[i, j, k] = int(med)
        # fortran 라이브러리 호출
        img_median = blur.median_filter(self.img, h=self.img_height_origin, w=self.img_width_origin, nf=3)
        img_median = np.require(img_median, np.uint8, 'C')  # fortran array to numpy array
        self.img2label(img_median)
        QApplication.restoreOverrideCursor()

    def blur_gaussian(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        img_gauss = blur.gauss_filter(self.img, self.img_height_origin, self.img_width_origin)
        img_gauss = np.require(img_gauss, np.uint8, 'C')
        self.img2label(img_gauss)
        QApplication.restoreOverrideCursor()

    def shift_east(self):
        _tmp = np.zeros((self.img_height_origin, 100, 3))  # 높이 h, 너비 pixel 인 빈 이미지를 만든다.
        self.img = np.concatenate((_tmp, self.img), axis=1)  # 좌측에 빈 이미지, 우측에 원본 이미지를 연결한 후,
        self.img =self.img[:, :self.img_width_origin, :].astype('uint8')  # 이미지 우측을 자른다.
        self.img2label(self.img)

    def shift_west(self):
        _tmp = np.zeros((self.img_height_origin, 100, 3))  # 높이 h, 너비 pixel 인 빈 이미지를 만든다.
        self.img = np.concatenate((self.img, _tmp), axis=1)  # 좌측에 원본 이미지, 우측에 빈 이미지를 연결한 후,
        self.img = self.img[:,100:,:].astype('uint8')  # 이미지 좌측을 자른다.
        self.img2label(self.img)

    def shift_south(self):
        _tmp = np.zeros((100, self.img_width_origin, 3)) # 높이 pixel, 너비 w 인 빈 이미지를 만든다.
        self.img = np.concatenate((_tmp, self.img), axis=0)  # 위쪽에 빈 이미지, 밑에 원본 이미지를 연결한 후,
        self.img = self.img[:self.img_height_origin, :, :].astype('uint8')  # 이미지 아래쪽을 자른다.
        self.img2label(self.img)

    def shift_north(self):
        _tmp = np.zeros((100, self.img_width_origin, 3))  # 높이 pixel, 너비 w 인 빈 이미지를 만든다.
        self.img = np.concatenate((self.img, _tmp), axis=0)  # 밑에 빈 이미지, 위에 원본 이미지를 연결한 후,
        self.img = self.img[100:, :, :].astype('uint8')  # 이미지 윗쪽을 자른다.
        self.img2label(self.img)

    def folderSelect(self):
        dirName = QFileDialog.getExistingDirectory(self, 'Open Folder', 'D:/NaverCloud/lecture/pywork/swexer2020/images')
        self.files = []
        for file in glob.glob(os.path.join(dirName, '*.jpg')):
            self.files.append(file)

        self.qPixmapVar = QPixmap(self.file2QImage(self.files[0]))
        self.qPixmapVar = self.qPixmapVar.scaled(self.hh, self.ww, aspectRatioMode=True)
        self.label.setPixmap(self.qPixmapVar)

    def file2QImage(self, fName):
        img = cv2.imread(fName)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)

    def img2QImage(self, img):
        return QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)

    def moveNextClick(self):
        self.idx += 1
        if self.idx == len(self.files):
            self.idx = 0
        self.qPixmapVar = QPixmap(self.file2QImage(self.files[self.idx]))
        self.qPixmapVar = self.qPixmapVar.scaled(self.hh, self.ww, aspectRatioMode=True)
        self.label.setPixmap(self.qPixmapVar)

app = QApplication(sys.argv)
myWindow = ViewerClass(None)
myWindow.show()
app.exec_()
