# -*- coding: utf-8 -*-
"""
This example demonstrates ViewBox and AxisItem configuration to plot a correlation matrix.
"""

from json.tool import main
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, mkQApp, QtGui
from PyQt5 import QtCore
import threading
import serial
import sys
# from skimage import transform


def flip90_right(arr):
    new_arr = arr.reshape(arr.size)
    new_arr = new_arr[::-1]
    new_arr = new_arr.reshape(arr.shape)
    new_arr = np.transpose(new_arr)[::-1]
    return new_arr


def Serial():
    global corrMatrix

    while True:
        try:
            response2 = ser.readline()
            row = response2.decode('utf-8').rstrip('\n').split(';')
            print(row)
            row[0] = row[0][5:]
            row = row[:100]
            row = [int(num) for num in row]

            for i in range(len(row)):
                # if row[i] >2500:
                #     row[i] = 2500
                row[i] =( row[i] - row0[i])
                # if row[i] <  0:
                #     row[i] = abs(row[i])

            row = np.array(row)/1000
            # print(row)
            corrMatrix = row.reshape((10, 10))
            # corrMatrix = flip90_right(corrMatrix1)
            # xx,yy = np.mgrid[0:9:100j,0:9:100j]
            # corrMatrix = transform.resize(corrMatrix, (30, 30), order=3)
            ser.flushInput()
            print(corrMatrix)
        except KeyboardInterrupt:
            ser.close()
            quit()
        except:
            print('fail receiving')


def setImageItem(coorelogram):
    bar.setImageItem(coorelogram, insert_in=plotItem)


# 映射强度矩阵
def circle(Matrix):
    corrMatrix[5, 5] = Matrix[0, 7]
    corrMatrix[6, 5] = Matrix[0, 7]
    corrMatrix[7, 5] = Matrix[0, 0]
    corrMatrix[7, 4] = Matrix[1, 0]
    corrMatrix[6, 4] = Matrix[2, 0]
    corrMatrix[5, 4] = Matrix[3, 0]
    corrMatrix[4, 4:7] = Matrix[4:7, 0]
    corrMatrix[5:8, 6] = Matrix[7:, 0]

    corrMatrix[8, 5] = Matrix[0, 1]
    corrMatrix[8, 4] = Matrix[1, 1]
    corrMatrix[8, 3] = Matrix[1, 1]
    corrMatrix[6, 3] = Matrix[2, 1]
    corrMatrix[7, 3] = Matrix[2, 1]
    corrMatrix[5, 3] = Matrix[3, 1]
    corrMatrix[4, 3] = Matrix[3, 1]
    corrMatrix[3, 3] = Matrix[4, 1]
    corrMatrix[3, 4] = Matrix[4, 1]
    corrMatrix[3, 5] = Matrix[5, 1]
    corrMatrix[3, 6] = corrMatrix[3, 7] = Matrix[6, 1]
    corrMatrix[4, 7] = corrMatrix[5, 7] = Matrix[7, 1]
    corrMatrix[6, 7] = corrMatrix[7, 7] = Matrix[8, 1]
    corrMatrix[8, 7] = corrMatrix[8, 6] = Matrix[9, 1]

    corrMatrix[9, 5] = Matrix[0, 3]
    corrMatrix[9, 4] = Matrix[0, 2]
    corrMatrix[9, 3] = Matrix[1, 3]
    corrMatrix[7, 2] = Matrix[1, 2]
    corrMatrix[6, 2] = Matrix[2, 3]
    corrMatrix[5, 2] = Matrix[2, 2]
    corrMatrix[4, 2] = Matrix[3, 3]
    corrMatrix[3, 2] = Matrix[3, 2]
    corrMatrix[2, 3] = Matrix[4, 3]
    corrMatrix[2, 4] = Matrix[4, 2]
    corrMatrix[2, 5] = Matrix[5, 3]
    corrMatrix[2, 6] = Matrix[5, 2]
    corrMatrix[2, 7] = Matrix[6, 3]
    corrMatrix[3, 8] = Matrix[6, 2]
    corrMatrix[4, 8] = Matrix[7, 3]
    corrMatrix[5, 8] = Matrix[7, 2]
    corrMatrix[6, 8] = Matrix[8, 3]
    corrMatrix[7, 8] = Matrix[8, 2]
    corrMatrix[9, 7] = Matrix[9, 3]
    corrMatrix[9, 6] = Matrix[9, 2]

    corrMatrix[10, 5] = Matrix[0, 5]
    corrMatrix[10, 4] = Matrix[0, 4]
    corrMatrix[10, 3] = Matrix[1, 5]
    corrMatrix[7, 1] = Matrix[1, 4]
    corrMatrix[6, 1] = Matrix[2, 5]
    corrMatrix[5, 1] = Matrix[2, 4]
    corrMatrix[4, 1] = Matrix[3, 5]
    corrMatrix[3, 1] = Matrix[3, 4]
    corrMatrix[1, 3] = Matrix[4, 5]
    corrMatrix[1, 4] = Matrix[4, 4]
    corrMatrix[1, 5] = Matrix[5, 5]
    corrMatrix[1, 6] = Matrix[5, 4]
    corrMatrix[1, 7] = Matrix[6, 5]
    corrMatrix[3, 9] = Matrix[6, 4]
    corrMatrix[4, 9] = Matrix[7, 5]
    corrMatrix[5, 9] = Matrix[7, 4]
    corrMatrix[6, 9] = Matrix[8, 5]
    corrMatrix[7, 9] = Matrix[8, 4]
    corrMatrix[10, 7] = Matrix[9, 5]
    corrMatrix[10, 6] = Matrix[9, 4]

    corrMatrix[11, 5] = Matrix[0, 6]
    corrMatrix[11, 4] = Matrix[1, 6]
    corrMatrix[6, 0] = Matrix[2, 6]
    corrMatrix[5, 0] = Matrix[3, 6]
    corrMatrix[0, 4] = Matrix[4, 6]
    corrMatrix[0, 5] = Matrix[5, 6]
    corrMatrix[0, 6] = Matrix[6, 6]
    corrMatrix[5, 10] = Matrix[7, 6]
    corrMatrix[6, 10] = Matrix[8, 6]
    corrMatrix[11, 6] = Matrix[9, 6]


# 更新数据
def plotData():
    global corrMatrix
    global coe
    try:
        response = ser.readline()
        row = response.decode('utf-8')[5:-3].split(';')
        Matrix = np.array(row).astype(int).reshape((10, 10))
        Matrix = Matrix - Matrix0
        Matrix = np.where(Matrix < 50, 0, Matrix)
        Matrix = Matrix * coe

        print(Matrix)
        Matrix = Matrix / 1000
        circle(Matrix)
    except KeyboardInterrupt:
        ser.close()
        quit()
    except:
        print('fail receiving')
    correlogram.setImage(corrMatrix)
    bar.setImageItem(correlogram, insert_in=plotItem)  


# Start Qt event loop
if __name__ == '__main__':
    # 初始化灵敏度矩阵
    coe = np.ones((10, 10))

    # 读取串口数据
    ser = serial.Serial('COM3', 115200, timeout=1)
    ser.close()
    ser.open()

    # 计算初始电压
    count = 0
    temp = np.zeros(100)
    while count < 10:
        try:
            response0 = ser.readline()
            row0 = response0.decode('utf-8')[5:-3].split(';')
            temp += np.array(row0).astype(int)
            print('initial:{}'.format(count))
            count += 1
        except KeyboardInterrupt:
            ser.close()
            quit()
        except Exception as e:
            print(e)
    Matrix0 = (temp / count).reshape((10, 10))
    print(Matrix0)

    # 显示强度图
    # 高分屏时需要设置
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = mkQApp("Correlation matrix display")
    pg.setConfigOption('background', 'w')
    main_window = QtWidgets.QMainWindow()
    gr_wid = pg.GraphicsLayoutWidget(show=True)
    main_window.setCentralWidget(gr_wid)
    main_window.setWindowTitle('Tactile Arrays')
    main_window.resize(700, 600)  # 600,500
    main_window.show()

    corrMatrix = np.ones((12, 11))*0.9
    columns = list(range(1, 12))

    # Switch default order to Row-major# 对于'row-major'，图像数据应按标准（行，列）顺序。
    # 对于'col-major'，图像数据应以相反的（col，row）顺序。
    pg.setConfigOption('imageAxisOrder', 'row-major')

    # given a QTransform, return a 3x3 numpy array. Given a QMatrix4x4, return a 4x4 numpy array.
    tr = QtGui.QTransform().translate(12, 11)
    correlogram = pg.ImageItem()
    # create transform to center the corner element on the origin, for any assigned image:
    # 对于任何指定的图像，创建变换以使角点元素在原点上居中：
    correlogram.setTransform(tr)

    colorMap = pg.colormap.get("magma")  # choose perceptually uniform, diverging color map选择感知上一致的、发散的颜色图
    # generate an adjustabled color bar, initially spanning -1 to 1:
    bar = pg.ColorBarItem(values=(0, 1), colorMap=colorMap)

    plotItem = gr_wid.addPlot()  # add PlotItem to the main GraphicsLayoutWidget
    plotItem.invertY(True)  # orient y axis to run top-to-bottom
    plotItem.setDefaultPadding(0.0)  # plot without padding data range 设置自动测距时用于填充视图范围的数据范围分数
    plotItem.addItem(correlogram)  # display correlogram

    # show full frame, label tick marks at top and left sides, with some extra space for labels:
    plotItem.showAxes(True, showValues=(True, True, False, False), size=20)

    # define major tick marks and labels:
    ticks = [(idx, label) for idx, label in enumerate(columns)]
    for side in ('left', 'top', 'right', 'bottom'):
        plotItem.getAxis(side).setTicks((ticks, []))  # add list of major ticks; no minor ticks
    plotItem.getAxis('bottom').setHeight(10)  # include some additional space at bottom of figure

    # link color bar and color map to correlogram, and show it in plotItem:
    correlogram.setImage(corrMatrix)
    bar.setImageItem(correlogram, insert_in=plotItem)

    # th1 = threading.Thread(target=Serial)
    # th1.start()
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(plotData)
    timer.start(1)
    sys.exit(app.exec())
    # pg.exec()
