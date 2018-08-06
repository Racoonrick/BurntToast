from data_handling.db_handle import db_handle as dbh
from analysis.Derivative import Derivative
import sqlite3
import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QSlider
from PyQt5.QtGui import QIcon, QWheelEvent
#******************************************************************
import matplotlib
matplotlib.use("Qt5Agg")
#******************************************************************
from PyQt5 import QtCore 
import math
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
class App(QMainWindow):
 
	def __init__(self):
		super().__init__()
		self.left = 100
		self.top = 100
		self.title = 'Burnt Toast - BTC Visual'
		self.width = 900
		self.height = 620
		
		self.initUI()


	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.m = PlotCanvas(self, width=5, height=4)
		self.m.move(0,0)

		button = QPushButton('Refresh', self)
		button.setToolTip('This s an example button')
		button.move(750,0)
		button.resize(70,50)
		button.clicked.connect(self.on_click)

		button2 = QPushButton('Reset Plot', self)
		button2.setToolTip('Set offset to 0')
		button2.move(820,0)
		button2.resize(70,50)
		button2.clicked.connect(self.reset_plot)

		#This is the zoom slider initialization
		self.sl = QSlider(QtCore.Qt.Horizontal,self)
		self.sl.move(0,550)
		self.sl.sliderReleased.connect(self.sl_zoom_release)

		#This is the shift slider initialization
		self.s2 = QSlider(QtCore.Qt.Horizontal,self)
		self.s2.move(0,580)
		self.s2.resize(200,50)
		self.s2.sliderReleased.connect(self.sl_shift_release)

		self.x = 0

		self.show()
	def sl_zoom_release(self):
		self.m.SlZoom(self.sl.value())

	def sl_shift_release(self):
		self.m.SlideShift(self.s2.value())

	def on_click(self):
		self.m.plot()

	def reset_plot(self):
		self.m.DefaultPlot()
	def wheelEvent(self, event):
		slide_boost = 300
		self.x = slide_boost*event.angleDelta().y()/120
		self.m.WheelShift(self.x)


class PlotCanvas(FigureCanvas):
 
	def __init__(self, parent=None, width=5, height=4, dpi=150):
		self.d1 = 0
		self.d2 = 0
		#This sets the maximum time you will see
		#from the recorded database
		self.full_window = 1*24*60*60
		self.pricev,self.sizev,self.timev = self.ParseData()
		self.mpricev,self.msizev,self.mtimev = self.ParseMyTrade()
		self.xa = min(self.timev)
		self.xb = max(self.timev)
		self.xcenter = (self.xb-self.xa)/2+self.xa
		self.min_x = self.xa
		self.max_x = self.xb
		self.x_wid = self.max_x - self.min_x
		
		########################################
		#Initialization for Linear Regression
		self.fitWindow = 30*60
		########################################

		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)

		FigureCanvas.__init__(self, fig)
		self.setParent(parent)

		FigureCanvas.setSizePolicy(self,
				QSizePolicy.Expanding,
				QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		self.plot()

	def update_plot(self):
		ax = self.figure.add_subplot(111)
		ax.figure.clear()
		ax = self.figure.add_subplot(111)
		ax.axes.set_xlim(self.xa,self.xb)
		ax.axes.set_ylim(min(self.pricev)-100,max(self.pricev)+100)
		ax.plot(self.timev,self.pricev, 'r-',linewidth=0.2)
		ax.plot(self.mtimev,self.mpricev, 'go',linewidth=5)
		ax.plot(self.xfit,self.yfit,'b-',linewidth=.2)


		ax.set_title('BTC Trade Information')
		self.draw()

	def plot(self):
		self.pricev,self.sizev,self.timev = self.ParseData()
		self.mpricev,self.msizev,self.mtimev = self.ParseMyTrade()
		self.xfit,self.yfit = self.LinearFit(self.fitWindow)
		self.alen = len(self.timev)
		self.min_x = min(self.timev)
		self.max_x = max(self.timev)
		self.x_wid = self.max_x - self.min_x
		self.update_plot()

	def LinearFit(self,fitWindow):
		slope,intercept,xfit = Derivative().FitDataLinear(fitWindow,self.timev,self.pricev)
		yfit = [i*slope+intercept for i in xfit]
		return xfit, yfit

	def SlZoom(self,sl_val=10):

		if sl_val == 100:
			scale = (99/100)
		else:
			scale = ((100-sl_val)/100)
		if self.xcenter - self.x_wid/2*scale > self.min_x :
			self.xa = self.xcenter - self.x_wid/2*scale
		else:
			self.xa = self.min_x
		if self.xcenter + self.x_wid/2*scale < self.max_x:
			self.xb = self.xcenter + self.x_wid/2*scale
		else:
			self.xb = self.max_x
		self.update_plot()

	def SlideShift(self,sl_slide):
		#Slider shift control
		window_x = self.max_x - self.min_x
		scale = sl_slide/100
		newcenter = window_x * scale + self.min_x
		oldcenter = (self.xb-self.xa)/2+self.xa
		sl_shift = newcenter-oldcenter
		if self.xa + sl_shift > self.min_x:
			self.xa = self.xa + sl_shift
		else:
			self.xa = self.min_x

		if self.xb + sl_shift < self.max_x:
			self.xb = self.xb + sl_shift
		else:
			self.xb = self.max_x-1
		self.xcenter = newcenter
		self.update_plot()

	def WheelShift(self,sl_slide):
		if self.xa + sl_slide > self.min_x:
			self.xa = self.xa + sl_slide
		else:
			self.xa = self.min_x

		if self.xb + sl_slide < self.max_x:
			self.xb = self.xb + sl_slide
		else:
			self.xb = self.max_x-1
		self.xcenter = (self.xb-self.xa)/2+self.xa

		self.update_plot()
	def DefaultPlot(self):
		self.xa = min(self.timev)
		self.xb = max(self.timev)
		self.xcenter = (self.xb-self.xa)/2+self.xa
		self.min_x = self.xa
		self.max_x = self.xb
		self.x_wid = self.max_x - self.min_x
		self.update_plot()

	def ParseMyTrade(self):
		db_path ="C:/Users/Ricky/Documents/Work/BurntToast/data_handling/fake_trades"
		tname = 'trades'
		tcolumns = '(sequence integer, price real, size real, time real)'
		algo_dbh = dbh(db_path,tname,tcolumns)
		algo_dbh.c.execute('SELECT price, size, time FROM trades')
		data = algo_dbh.c.fetchall()

		pricev = []
		sizev = []
		timev = []
		for row in data:
			pricev.append(row[0])
			sizev.append(row[1])
			timev.append(row[2])

		return pricev,sizev,timev;

	def ParseData(self):
		db_path ="C:/Users/Ricky/Documents/Work/BurntToast/exchange_hook/websocket_trades_db"
		tname = 'trades'
		tcolumns = '(sequence integer, price real, size real, time real)'
		algo_dbh = dbh(db_path,tname,tcolumns)
		algo_dbh.c.execute('SELECT price, size, time FROM trades')
		data = algo_dbh.c.fetchall()

		#print(data)
		pricev = []
		sizev = []
		timev = []

		for row in data:
			pricev.append(row[0])
			sizev.append(row[1])
			timev.append(row[2])

		chopindex = Derivative().FrameTime(self.full_window,timev)
		return pricev[-chopindex:],sizev[-chopindex:],timev[-chopindex:];


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())