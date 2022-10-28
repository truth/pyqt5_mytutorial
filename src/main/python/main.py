import time

from PyQt5.QtNetwork import QNetworkProxyFactory
from PyQt5.QtWidgets import QApplication, QGraphicsDropShadowEffect
# from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout, QLabel, QPushButton, QSizePolicy, QGraphicsView, \
    QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QTimer, QFile
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineScript
import cv2
import numpy as np
import threading
import sys
from MyChartView import MyChartView
from MyWebView import MyWebView
from QSSLoader import QSSLoader
from qt_material import apply_stylesheet

import configparser
config = configparser.ConfigParser() # 类实例化

class MyApp:
    cap = None
    count = 0
    is_run = False

    def __int__(self):
        self.count = 1

    def open(self):
        self.is_run = True
        # rtsp://admin:nutshell123456@192.168.20.198/h264/chn1/sub/av_stream
        # rtsp://192.168.20.11:58554/live/car2
        videoUrl = config.get("default","videoUrl")
        self.cap = cv2.VideoCapture(videoUrl)
        self.cap.set(cv2.CAP_PROP_XI_TIMEOUT, 100)
        # print(self.cap.isOpened())
        return self.cap.isOpened()

    def close(self):
        if self.cap is not None:
            self.cap.release()
        self.is_run = False

    def restart(self):
        self.close()
        time.sleep(2)
        self.open()


class MyWidget(QWidget):
    app = MyApp()
    timer = QTimer()
    is_resize = False

    def __init__(self):
        super(MyWidget, self).__init__(None)  # 设置为顶级窗口，无边框
        self.webview = None
        self.ready = False
        self.chart_view_blue = None
        self.chart_view_green = None
        self.chart_view = None
        self.view_item = None
        self.btn_exit = None
        self.btn_full = None
        self.start = None
        self.label = None
        self.pix = None
        self.video_view = None
        self.scene = None
        self.frame = None

    def init(self):
        QNetworkProxyFactory.setUseSystemConfiguration(False);
        self.label = QLabel("消息区")
        self.scene = QGraphicsScene()
        self.video_view = QGraphicsView()
        self.video_view.setScene(self.scene)
        self.setWindowTitle("视频测试")
        # self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QGridLayout()
        self.timer.timeout.connect(self.time_out)
        # timer.start(20)
        self.webview = MyWebView()
        # file:///E:/Python/PycharmProjects/pyqt5/index.html
        # self.webview.settings.setUserStyleSheetUrl(QUrl("./scrollbarstyle.css"));
        url = config.get('default', 'url')
        self.webview.setGraphicsEffect(QGraphicsDropShadowEffect())
        self.webview.graphicsEffect().setEnabled(False);
        self.webview.load(QUrl(url))
        self.start = QPushButton("Start")
        self.btn_full = QPushButton("全屏")
        self.btn_exit = QPushButton("退出全屏")
        self.start.clicked.connect(self.start_click)
        self.btn_full.clicked.connect(self.btnfull_click)
        self.btn_exit.clicked.connect(self.btnexit_click)
        layout.addWidget(self.video_view, 0, 0, 2, 3)
        layout.addWidget(self.webview, 2, 0, 1, 3)
        self.chart_view = MyChartView()
        self.chart_view.init()
        self.chart_view_green = MyChartView()
        self.chart_view_green.init()
        self.chart_view_blue = MyChartView()
        self.chart_view_blue.init()
        layout.addWidget(self.chart_view.graphicsView, 0, 3, 1, 1)
        layout.addWidget(self.chart_view_green.graphicsView, 1, 3, 1, 1)
        layout.addWidget(self.chart_view_blue.graphicsView, 2, 3, 1, 1)
        layout.addWidget(self.start, 3, 0)
        layout.addWidget(self.btn_full, 3, 1)
        layout.addWidget(self.btn_exit, 3, 2)
        layout.addWidget(self.label, 3, 3)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)
        self.setLayout(layout)
        # self.chart_view.add_data()

    def run_thread(self):
        print(self.app.open())
        t = time.perf_counter()
        while self.app.is_run:
            if self.app.cap.isOpened():
                success, self.frame = self.app.cap.read()
                ftime = time.perf_counter() - t
                print(f'per frame time:{ftime:.4f}s')
                t = time.perf_counter()
                # (b, g, r) = cv2.split(frame)
                # bH = cv2.equalizeHist(b)
                # gH = cv2.equalizeHist(g)
                # rH = cv2.equalizeHist(r)
                # # 合并每一个通道
                # equ2 = cv2.merge((bH, gH, rH))
                # result2 = np.hstack((frame, equ2))
                if not success:
                    self.label.setText(f"restart:{self.app.count}")
                    self.app.restart()
                    self.label.setText(f"start ok!")
                    continue
                frame2 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                q_img = QImage(frame2.data, frame2.shape[1], frame2.shape[0], frame2.shape[1] * 3, QImage.Format_RGB888)
                # self.rhist = cv2.calcHist([frame], [2], None, [256], [0, 256])
                # if self.is_resize:
                #     self.label.resize(400, 400)
                #     self.resize(640, 480)
                #     self.is_resize = False
                #     self.pix = QPixmap(q_img).scaled(400, 400)
                #
                # else:
                self.pix = QPixmap(q_img).scaled(self.video_view.width() - 2, self.video_view.height() - 2)
                # 获取当前view的Rect
                view_rect = self.video_view.contentsRect()
                # 计算scene的Rect，因为我将图片图元居中显示，所以我将偏移计算在左右、上下居中位置
                # s_x = int(abs(view_rect.width() - self.image_w) / 2)
                # s_y = int(abs(view_rect.height() - self.image_h) / 2)
                self.video_view.setSceneRect(-1, -1, view_rect.width(), view_rect.height())
                self.update()
                self.ready = True
                self.label.setText(f"time:{ftime:.4f}s")
            else:
                self.label.setText(f"cap is error!{self.app.count}")
                self.app.close()
                print(self.app.open())
            time.sleep(0.01)

    def paintEvent(self, event):
        if not self.ready:
            return
        if self.pix is not None:
            if self.view_item is not None:
                self.scene.removeItem(self.view_item)
            self.view_item = self.scene.addPixmap(self.pix)
            self.video_view.update()
            self.chart_view_blue.update(self.frame, 0)
            self.chart_view_green.update(self.frame, 1)
            self.chart_view.update(self.frame, 2)
            self.ready = False
        return

    def start_click(self):
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
    appctxt = QApplication(sys.argv)  # 1. Instantiate ApplicationContext
    config.read("./config.ini")
    # create the application and the main window
    from qt_material import list_themes

    list_themes()
    # setup stylesheet
    apply_stylesheet(appctxt, theme='default_dark.xml')
    # style_file = 'E:/Python/PycharmProjects/pyqt5/src/main/python/Behave-dark.qss'
    # style_sheet = QSSLoader.read_qss_file(style_file)
    window = MyWidget()
    window.init()
    #  window.setStyleSheet(style_sheet)
    window.resize(600, 400)
    window.show()
    exit_code = appctxt.exec_()  # 2. Invoke appctxt.app.exec_()
    window.close_app()
    sys.exit(exit_code)
