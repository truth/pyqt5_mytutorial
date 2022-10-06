import time

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout, QLabel, QPushButton, QSizePolicy, QGraphicsView,\
    QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np
import threading
import sys


class MyApp:
    cap = None
    count = 0
    is_run = False

    def __int__(self):
        self.count = 1

    def open(self):
        self.is_run = True
        self.cap = cv2.VideoCapture("rtsp://admin:nutshell123456@192.168.22.178/h264/chn1/main/av_stream")
        # print(self.cap.isOpened())
        return self.cap.isOpened()

    def close(self):
        self.cap.release()
        self.is_run = False


class MyWidget(QWidget):
    app = MyApp()
    timer = QTimer()
    is_resize = False

    def __init__(self):
        super(MyWidget, self).__init__(None)  # 设置为顶级窗口，无边框
        self.view_item = None
        self.btn_exit = None
        self.btn_full = None
        self.start = None
        self.label = None
        self.pix = None
        self.video_view = None
        self.scene = None

    def init(self):
        self.label = QLabel("当前时间")
        self.scene = QGraphicsScene()
        self.video_view = QGraphicsView()
        self.video_view.setScene(self.scene)
        self.setWindowTitle("视频测试")
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QGridLayout()
        self.timer.timeout.connect(self.time_out)
        # timer.start(20)
        self.start = QPushButton("Start")
        self.btn_full = QPushButton("全屏")
        self.btn_exit = QPushButton("退出全屏")
        self.start.clicked.connect(self.start_click)
        self.btn_full.clicked.connect(self.btnfull_click)
        self.btn_exit.clicked.connect(self.btnexit_click)
        layout.addWidget(self.video_view, 0, 0, 1, 3)
        layout.addWidget(self.start, 1, 0)
        layout.addWidget(self.btn_full, 1, 1)
        layout.addWidget(self.btn_exit, 1, 2)
        self.setLayout(layout)

    def run_thread(self):
        while self.app.is_run:
            if self.app.cap.isOpened():
                success, frame = self.app.cap.read()
                (b, g, r) = cv2.split(frame)
                bH = cv2.equalizeHist(b)
                gH = cv2.equalizeHist(g)
                rH = cv2.equalizeHist(r)
                # 合并每一个通道
                equ2 = cv2.merge((bH, gH, rH))
                # result2 = np.hstack((frame, equ2))
                frame2 = cv2.cvtColor(equ2, cv2.COLOR_BGR2RGB)
                q_img = QImage(frame2.data, frame2.shape[1], frame2.shape[0], frame2.shape[1] * 3, QImage.Format_RGB888)


                # if self.is_resize:
                #     self.label.resize(400, 400)
                #     self.resize(640, 480)
                #     self.is_resize = False
                #     self.pix = QPixmap(q_img).scaled(400, 400)
                #
                # else:
                self.pix = QPixmap(q_img).scaled(self.video_view.width()-2, self.video_view.height()-2)
                # 获取当前view的Rect
                view_rect = self.video_view.contentsRect()
                # 计算scene的Rect，因为我将图片图元居中显示，所以我将偏移计算在左右、上下居中位置
                # s_x = int(abs(view_rect.width() - self.image_w) / 2)
                # s_y = int(abs(view_rect.height() - self.image_h) / 2)
                self.video_view.setSceneRect(-1, -1, view_rect.width(), view_rect.height())

            else:
                self.label.setText(f"cap is error!{self.app.count}")
            time.sleep(0.002)

    def paintEvent(self, event):
        if self.pix is not None:
            if self.view_item is not None:
                self.scene.removeItem(self.view_item)
            self.view_item = self.scene.addPixmap(self.pix)
            self.video_view.update()


    def start_click(self):
        print(self.app.open())
        t1 = threading.Thread(target=self.run_thread)
        t1.start()

    def btnfull_click(self):
        self.showFullScreen()

    def btnexit_click(self):
        self.showNormal()

    def time_out(self):
        self.app.count += 1
        if self.app.cap.isOpened():
            success, frame = self.app.cap.read()
            (b, g, r) = cv2.split(frame)
            bH = cv2.equalizeHist(b)
            gH = cv2.equalizeHist(g)
            rH = cv2.equalizeHist(r)
            # 合并每一个通道
            equ2 = cv2.merge((bH, gH, rH))
            # result2 = np.hstack((frame, equ2))
            frame2 = cv2.cvtColor(equ2, cv2.COLOR_BGR2RGB)
            q_img = QImage(frame2.data, frame2.shape[1], frame2.shape[0], frame2.shape[1] * 3, QImage.Format_RGB888)
            pix = QPixmap(q_img).scaled(self.label.width(), self.label.height())
            self.label.setPixmap(pix)
        else:
            self.label.setText(f"cap is error!{self.app.count}")

    def close_app(self):
        self.app.close()


if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext

    window = MyWidget()
    window.init()
    window.resize(600, 400)
    window.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    window.close_app()
    sys.exit(exit_code)
