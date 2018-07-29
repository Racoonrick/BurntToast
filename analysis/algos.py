# from data_handling.db_handle import db_handle as dbh
# import sqlite3
# import sys
# import matplotlib
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure 
# from matplotlib import style


# db_path ="C:/Users/Ricky/Documents/Work/BurntToast/exchange_hook/websocket_trades_db"
# tname = 'trades'
# tcolumns = '(sequence integer, price real, size real, time real)'
# algo_dbh = dbh(db_path,tname,tcolumns)
# #algo_dbh.conn.execute('SELECT * FROM trades ORDER BY sequence ASC')
# algo_dbh.c.execute('SELECT price, size, time FROM trades')
# #algo_dbh.print_trades()
# data = algo_dbh.c.fetchall()

# #print(data)
# pricev = []
# sizev = []
# timev = []
# for row in data:
# 	pricev.append(row[0])
# 	sizev.append(row[1])
# 	timev.append(row[2])

# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.set_title("Price vs Time")
# ax1.set_ylabel("Price [$]")
# ax1.set_xlabel("Time [s]")
# plt.figure()
# plt.plot(timev,pricev,'-',label="Price",color='red')
# ax1.plot(timev,pricev,'-',label="Price",color='red')

from data_handling.db_handle import db_handle as dbh
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
		self.title = 'PyQt5 matplotlib example - pythonspot.com'
		self.width = 900
		self.height = 600
		
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

		self.sl = QSlider(QtCore.Qt.Horizontal,self)
		self.sl.move(0,550)
		self.sl.sliderReleased.connect(self.sl_release)

		self.x = 0

		self.show()
	def sl_release(self):
		print(self.sl.value())
		self.m.SlZoom(self.sl.value())

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
		self.pricev,self.sizev,self.timev = self.ParseData()
		self.mpricev,self.msizev,self.mtimev = self.ParseMyTrade()
		self.xa = min(self.timev)
		self.xb = max(self.timev)
		self.xcenter = (self.xb-self.xa)/2+self.xa
		print(self.xcenter)
		self.min_x = self.xa
		self.max_x = self.xb
		self.x_wid = self.max_x - self.min_x
		print(self.x_wid)
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
		ax.plot(self.timev[:],self.pricev[:], 'r-',linewidth=0.2)
		ax.plot(self.mtimev[:],self.mpricev[:], 'go',linewidth=5)


		print(self.xa,self.xb)
		ax.set_title('PyQt Matplotlib Example')
		self.draw()

	def plot(self):
		self.pricev,self.sizev,self.timev = self.ParseData()
		self.mpricev,self.msizev,self.mtimev = self.ParseMyTrade()
		self.alen = len(self.timev)
		self.update_plot()
	
	def AxesScale(self):
		max_x = math.max(self.timev)
		min_x = math.min(self.timev)
		

	def SlZoom(self,sl_val=10):

		if sl_val == 100:
			scale = (99/100)
		else:
			scale = ((100-sl_val)/100)
		if self.xcenter - self.x_wid/2*scale > min(self.timev) :
			self.xa = self.xcenter - self.x_wid/2*scale
		else:
			self.xa = self.min_x
		if self.xcenter + self.x_wid/2*scale < max(self.timev):
			self.xb = self.xcenter + self.x_wid/2*scale
		else:
			self.xb = self.max_x
		print(self.xcenter)
		self.update_plot()

	def WheelShift(self,sl_slide):
		print(self.xa,self.xb)
		if self.xa + sl_slide > min(self.timev):
			self.xa = self.xa + sl_slide
		else:
			self.xa = min(self.timev)

		if self.xb + sl_slide < self.max_x:
			self.xb = self.xb + sl_slide
		else:
			self.xb = self.max_x-1
		self.xcenter = (self.xb-self.xa)/2+self.xa
		print("centerrrr",self.xcenter)

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

		self.max_x = max(timev)
		return pricev,sizev,timev;


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())