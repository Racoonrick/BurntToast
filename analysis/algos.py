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
		self.m.WheelZoom(self.x)
		print(self.x)

		


class PlotCanvas(FigureCanvas):
 
	def __init__(self, parent=None, width=5, height=4, dpi=150):
		self.a1 = 0 
		self.a2 = 500
		self.d1 = 0
		self.d2 = 0
		self.pricev,self.sizev,self.timev = self.ParseData()
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
		ax.plot(self.timev[self.a1:self.a2],self.pricev[self.a1:self.a2], 'r-',linewidth=0.2)
		ax.set_title('PyQt Matplotlib Example')
		self.draw()

	def plot(self):
		self.pricev,self.sizev,self.timev = self.ParseData()
		self.alen = len(self.timev)
		self.update_plot()
		
	def SlZoom(self,sl_val=10):
		amid = self.alen/2
		if sl_val == 100:
			self.scale = (99/100)
		else:
			self.scale = ((100-sl_val)/100)
		xsubt = self.alen*self.scale
		self.a1 = max(0,min(self.alen,math.ceil(self.alen-xsubt+self.d1)))
		self.a2 = math.ceil(min(self.alen,self.alen + self.d2))
		print(self.a1,self.a2)
		self.update_plot()

	def WheelZoom(self,sl_slide):
		self.d1 += sl_slide/self.scale
		self.d2 += sl_slide/self.scale
		self.a1 = math.ceil(self.a1 + sl_slide)
		self.a2 = math.ceil(self.a2 + sl_slide)
		self.update_plot()
	def DefaultPlot(self):
		self.a1 = 0
		self.a2 = self.alen
		self.d1,self.d2 = 0,0
		self.update_plot()

	def ParseData(self):
		db_path ="C:/Users/Ricky/Documents/Work/BurntToast/exchange_hook/websocket_trades_db"
		tname = 'trades'
		tcolumns = '(sequence integer, price real, size real, time real)'
		algo_dbh = dbh(db_path,tname,tcolumns)
		#algo_dbh.conn.execute('SELECT * FROM trades ORDER BY sequence ASC')
		algo_dbh.c.execute('SELECT price, size, time FROM trades')
		#algo_dbh.print_trades()
		data = algo_dbh.c.fetchall()

		#print(data)
		pricev = []
		sizev = []
		timev = []
		for row in data:
			pricev.append(row[0])
			sizev.append(row[1])
			timev.append(row[2])

		return pricev,sizev,timev;


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())

