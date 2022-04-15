# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from PyQt5.Qt import *
from pyqtgraph import PlotWidget, VerticalLabel
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLineEdit, QFormLayout
import numpy as np
import pyqtgraph as pq
import serial
import sys
import os


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.row = None
        # 设置下尺寸
        self.resize(800, 660)
        self.setWindowTitle('3D force sensor')

        # 添加 QWidget 控件
        self.text = QWidget(self)
        self.text.setGeometry(480, 350, 300, 200)
        self.text_fx = QLabel()
        self.text_fy = QLabel()
        self.text_fz = QLabel()
        lay = QFormLayout(self.text)
        lay.addRow('<font size="8">Fx(N): </font>', self.text_fx)
        lay.addRow('<font size="8">Fy(N): </font>', self.text_fy)
        lay.addRow('<font size="8">Fz(N): </font>', self.text_fz)

        # 添加 PlotWidget 控件
        self.plotWidget_vec = PlotWidget(self)
        self.plotWidget_fx = PlotWidget(self)
        self.plotWidget_fy = PlotWidget(self)
        self.plotWidget_fz = PlotWidget(self)

        # 设置该控件尺寸和相对位置
        self.plotWidget_vec.setGeometry(QtCore.QRect(480, 20, 300, 300))
        self.plotWidget_fx.setGeometry(QtCore.QRect(20, 20, 450, 200))
        self.plotWidget_fy.setGeometry(QtCore.QRect(20, 230, 450, 200))
        self.plotWidget_fz.setGeometry(QtCore.QRect(20, 440, 450, 200))

        # 生成 500 初始化数据
        self.ptr = 0
        self.data_fx = np.zeros(500)
        self.data_fy = np.zeros(500)
        self.data_fz = np.zeros(500)

        # 设置显示内容 添加plot
        # 方向窗口
        self.plotWidget_vec.setTitle('<font size="5", color="black"><b>Direction</b></font>')
        self.plotWidget_vec.hideAxis('bottom')
        self.plotWidget_vec.hideAxis('left')
        self.plotWidget_vec.addLine(x=0)
        self.plotWidget_vec.addLine(y=0)
        self.plotWidget_vec.setBackground(None)
        self.plotWidget_vec.setRange(xRange=(-1, 1), yRange=(-1, 1))
        self.curve_vec = self.plotWidget_vec.plot([0, 0], [0, 0], symbol='o')
        # 设置坐标轴
        b_x = pq.AxisItem('bottom', pen={'color': 'black', 'width': 1}, textPen={'color': 'black'})
        l_x = pq.AxisItem('left', pen={'color': 'black', 'width': 1}, textPen={'color': 'black'})
        b_y = pq.AxisItem('bottom', pen={'color': 'black', 'width': 1}, textPen={'color': 'black'})
        l_y = pq.AxisItem('left', pen={'color': 'black', 'width': 1}, textPen={'color': 'black'})
        b_z = pq.AxisItem('bottom', pen={'color': 'black', 'width': 1}, textPen={'color': 'black'})
        l_z = pq.AxisItem('left', pen={'color': 'black', 'width': 1}, textPen={'color': 'black'})
        # Fx 窗口
        self.plotWidget_fx.setAxisItems(axisItems={'bottom': b_x, 'left': l_x})
        self.plotWidget_fx.setYRange(-10, 10)
        self.plotWidget_fx.setLabel('left', text='<font size="5"><b>Fx (N)</b></font>')
        self.plotWidget_fx.setBackground(None)
        self.plotWidget_fx.showGrid(x=1, y=1)
        self.curve_fx = self.plotWidget_fx.plot(self.data_fx, pen={'color': (255, 0, 0), 'width': 3})
        # Fy 窗口
        self.plotWidget_fy.setAxisItems(axisItems={'bottom': b_y, 'left': l_y})
        self.plotWidget_fy.setYRange(-10, 10)
        self.plotWidget_fy.setLabel('left', text='<font size="5"><b>Fy (N)</b></font>')
        self.plotWidget_fy.setBackground(None)
        self.plotWidget_fy.showGrid(x=1, y=1)
        self.curve_fy = self.plotWidget_fy.plot(self.data_fy, pen={'color': (0, 255, 0), 'width': 3})
        # Fz 窗口
        self.plotWidget_fz.setAxisItems(axisItems={'bottom': b_z, 'left': l_z})
        self.plotWidget_fz.setYRange(-10, 20)
        self.plotWidget_fz.setLabel('left', text='<font size="5"><b>Fz (N)</b></font>')
        self.plotWidget_fz.setBackground(None)
        self.plotWidget_fz.showGrid(x=1, y=1)
        self.curve_fz = self.plotWidget_fz.plot(self.data_fz, pen={'color': (0, 0, 255), 'width': 3})

        # 设定定时器
        self.timer = pq.QtCore.QTimer()
        # 定时器信号绑定 update_data 函数
        self.timer.timeout.connect(self.update_data)
        # 定时器间隔50ms，可以理解为 50ms 刷新一次数据
        self.timer.start(1)

    # 数据左移
    def update_data(self):
        global ser
        try:
            response = ser.readline()
            row = response.decode('utf-8').rstrip('\n').split(',')
            if len(row) < 4 or row[0] == '':
                return
            row = np.array(row).astype(float)
            ser.flushInput()
            print(row)
        except Exception as e:
            print(e)
            return

        fx, fy, fz, vec = get_force(row[0], row[1], row[2], row[3])
        self.text_fx.setText('<font size="8">{}</font>'.format(fx))
        self.text_fy.setText('<font size="8">{}</font>'.format(fy))
        self.text_fz.setText('<font size="8">{}</font>'.format(fz))

        self.data_fx[:-1] = self.data_fx[1:]
        self.data_fx[-1] = fx

        self.data_fy[:-1] = self.data_fy[1:]
        self.data_fy[-1] = fy

        self.data_fz[:-1] = self.data_fz[1:]
        self.data_fz[-1] = fz
        # 数据填充到绘制曲线中
        self.ptr += 1
        self.curve_vec.setData([0, vec[0]], [0, vec[1]])

        self.curve_fx.setData(self.data_fx)
        self.curve_fx.setPos(self.ptr, 0)

        self.curve_fy.setData(self.data_fy)
        self.curve_fy.setPos(self.ptr, 0)

        self.curve_fz.setData(self.data_fz)
        self.curve_fz.setPos(self.ptr, 0)


def get_force(v1, v2, v3, v4):
    global v0
    f1 = 4.5*(v1 / 1000 - v0[0])
    f2 = 4.5*(v2 / 1000 - v0[1])
    f3 = 4.5*(v3 / 1000 - v0[2])
    f4 = 4.5*(v4 / 1000 - v0[3])
    if abs(f1) < 0.3:
        f1 = 0.
    if abs(f2) < 0.3:
        f2 = 0.
    if abs(f3) < 0.3:
        f3 = 0.
    if abs(f4) < 0.3:
        f4 = 0.
    fz = round(f1+f2+f3+f4, 3)
    fx = round(5*(f1-f4), 3)
    fy = round(5*(f2-f3), 3)
    vec = (fx/10, fy/10)
    return fx, fy, fz, vec


def read_data():
    global q
    global ser
    while True:
        try:
            ser.flushInput()
            response = ser.readline()
            row = np.array(response.decode('utf-8').rstrip('\n').split(',')).astype(int)
        except:
            return
        else:
            if len(row) < 3:
                return
        q.put(row)
        print(row)


if __name__ == '__main__':
    # 高分屏时需要设置
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    ser = serial.Serial('COM3', 115200, timeout=1)
    ser.close()
    ser.open()
    ser.flushInput()

    count = 0
    temp = np.zeros(4)
    while count < 10:
        try:
            response0 = ser.readline()
            row0 = np.array(response.decode('utf-8').rstrip('\n').split(',')).astype(int)
            temp += row0
            print('initial:{}'.format(count))
            count += 1
        except KeyboardInterrupt:
            ser.close()
            quit()
        except Exception as e:
            print(e)
    v0 = (temp / count / 1000)
    print(v0)

    # PyQt5 程序固定写法
    app = QApplication(sys.argv)

    # 将绑定了绘图控件的窗口实例化并展示
    window = Window()
    window.show()

    # PyQt5 程序固定写法
    sys.exit(app.exec())


