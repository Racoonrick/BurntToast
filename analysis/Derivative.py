from data_handling.db_handle import db_handle as dbh
import sqlite3
import sys
import time
import math

class Derivative:
	def __init__(self):
		# self.pricev,self.sizev,self.timev = self.ParseData()
		# self.mpricev,self.msizev,self.mtimev = self.ParseMyTrade()
		stuff = 0
	def ParseMyTrade(self):
		#Parses fake_trades data
		#these are trades user has made
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

		return pricev,sizev,timev

	def ParseData(self):
		#Parses all gdax exchange
		#data for btc
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
		return pricev,sizev,timev

	def FrameTime(self,xwindow,xval):
		#Searches xval in reverse order and 
		#breaks when it reaches the target tim.
		xmax = max(xval)
		xtarget = xmax-xwindow
		xindex = 1
		for i in reversed(xval[:]):
			if i < xtarget:
				break
			else:
				xindex+=1
		# print("Index Stop: ",xindex)
		# print("Max time: ",xmax)
		# print("Time window: ",xwindow)
		# print("Time target: ",xtarget)
		# print("Time found: ",xval[-tindex])
		return xindex


	def Mean(self,lista):
		return (sum(lista) / len(lista))
	def ListMult(self,lista,listb):
		return [a*b for a,b in zip(lista,listb)]
	def LinearRegression(self,xval,yval):
		#slope of regression:
		#	m = (  x.mean*y.mean - (x*y).mean  ) / (  x.mean^2 - x^2.mean  ) 
		#intercept of regression:
		#	b = y.mean - m * x.mean
		xmean	= self.Mean(xval)
		ymean	= self.Mean(yval)
		xymean	= self.Mean(self.ListMult(xval,yval))
		xsqmean	= self.Mean(self.ListMult(xval,xval))
		slope	= ( xmean * ymean - xymean ) / ( xmean * xmean - xsqmean )
		intercept = ymean-slope*xmean
		print("Slope: ",slope)
		print("Intercept: ",intercept)
		return slope,intercept

	def FitDataLinear(self,xwindow,xval,yval):
		xindex = self.FrameTime(xwindow,xval)
		xframe = xval[-xindex:]
		slope,intercept = self.LinearRegression(xframe,yval[-xindex:])
		return slope,intercept,xframe

if __name__ == '__main__':
	pricev,sizev,timev = Derivative().ParseData()
	# datax = [0,1,2,3,4,5]
	# datay = [1.1,1.5,1.55,1.48,1.65,1.66]
	slope,intercept,xframe = Derivative().FitDataLinear(15,timev,pricev)
	yframe = [i*slope+intercept for i in xframe]
	print(yframe)
	print(xframe)
	# print(derivdata.ListMult(datax,datax))
	# derivdata.LinearRegression(datax,datay)



