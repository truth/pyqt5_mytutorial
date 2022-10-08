from PyQt5.QtChart import QChartView, QLineSeries, QValueAxis, QAreaSeries, QChart
from PyQt5.QtGui import QPen, QLinearGradient, QColor
from PyQt5.QtCore import QPointF
from PyQt5.Qt import QGradient, Qt, QPainter

class MyChartView(object):
    is_refresh = True
    def __init__(self):
        self.area2 = None
        self.area1 = None
        self.vlaxisY = None
        self.dtaxisX = None
        self.series_temp = None
        self.series = None
        self.chart = None
        self.graphicsView = None
        self.x = [x for x in range(0, 255, 1)]

        self.lowerSeries = QLineSeries()
        for i in range(len(self.x )):
            self.lowerSeries.append(self.x[i], 0)

    def add_data(self):
        self.series.clear()
        self.series_temp.clear()

        self.series.append(0, 100)
        self.series.append(30, 200)
        self.series.append(60, 30)
        self.series.append(90, 80)
        self.series.append(120, 200)


        self.series_temp.append(0, 0)
        self.series_temp.append(30, 0)
        self.series_temp.append(60, 0)
        self.series_temp.append(90, 0)
        self.series_temp.append(120, 0)

        area = QAreaSeries(self.series, self.series_temp)
        area.setName("区域曲线")
        pen = QPen(Qt.red)
        pen.setWidth(1)
        area.setPen(pen)

        gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 1))
        gradient.setColorAt(0.0, QColor(255, 255, 255))
        gradient.setColorAt(1.0, QColor(0, 255, 0))
        gradient.setCoordinateMode(QGradient.ObjectBoundingMode)
        area.setBrush(gradient)
        self.chart.removeSeries(self.area1)
        self.area1 = area
        self.chart.addSeries(self.area1)

    def update(self,hist):
        if not self.is_refresh:
            return
        self.series.clear()
        for i in range(len(self.x)):
            self.series.append(self.x[i],hist[i])
        area = QAreaSeries(self.series, self.lowerSeries)
        area.setName("区域曲线")
        pen = QPen(Qt.red)
        pen.setWidth(1)
        area.setPen(pen)

        gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 1))
        gradient.setColorAt(0.0, QColor(255, 255, 255))
        gradient.setColorAt(1.0, QColor(0, 255, 0))
        gradient.setCoordinateMode(QGradient.ObjectBoundingMode)
        area.setBrush(gradient)
        if self.area1 is not None:
            self.chart.removeSeries(self.area1)
        self.area1 = area
        self.chart.addSeries(self.area1)
        self.is_refresh = False

    def init(self):
        self.chart = QChart()
        self.chart.setTitle('测试样例')
        self.series = QLineSeries()
        self.series.setName("压力")  # 设置曲线名称
        # self.chart.addSeries(self.series)  # 把曲线添加到QChart的实例中

        self.series_temp = QLineSeries()
        self.series_temp.setName("温度")  # 设置曲线名称
        # self.chart.addSeries(self.series_temp)  # 把曲线添加到QChart的实例中

        # 声明并初始化X轴、Y轴
        self.dtaxisX = QValueAxis()
        self.vlaxisY = QValueAxis()
        # 设置坐标轴显示范围
        self.dtaxisX.setMin(0)
        self.dtaxisX.setMax(256)
        self.vlaxisY.setMin(0)
        self.vlaxisY.setMax(250)
        # 设置坐标轴名称
        self.dtaxisX.setTitleText("X轴")
        self.vlaxisY.setTitleText("Y轴")
        # 把坐标轴添加到chart中
        self.chart.addAxis(self.dtaxisX, Qt.AlignBottom)
        self.chart.addAxis(self.vlaxisY, Qt.AlignLeft)
        # 把曲线关联到坐标轴
        self.series.attachAxis(self.dtaxisX)
        self.series.attachAxis(self.vlaxisY)
        self.series_temp.attachAxis(self.dtaxisX)
        self.series_temp.attachAxis(self.vlaxisY)

        # self.series.append(0, 100)
        # self.series.append(30, 200)
        # self.series.append(60, 30)
        # self.series.append(90, 80)
        # self.series.append(120, 200)
        #
        # self.series_temp.append(0, 0)
        # self.series_temp.append(30, 0)
        # self.series_temp.append(60, 0)
        # self.series_temp.append(90, 0)
        # self.series_temp.append(120, 0)

        # self.area1 = QAreaSeries(self.series, self.series_temp)
        # self.area1.setName("区域曲线")
        # pen = QPen(Qt.red)
        # pen.setWidth(1)
        # self.area1.setPen(pen)
        #
        # gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 1))
        # gradient.setColorAt(0.0, QColor(255, 255, 255))
        # gradient.setColorAt(1.0, QColor(0, 255, 0))
        # gradient.setCoordinateMode(QGradient.ObjectBoundingMode)
        # self.area1.setBrush(gradient)
        # self.chart.addSeries(self.area1)

        self.graphicsView = QChartView(self.chart)
        # self.graphicsView.setGeometry(widget.contentsRect())
        self.graphicsView.setObjectName("graphicsView")


