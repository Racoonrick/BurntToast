from data_handling.data_handle import data_handle
from data_handling.db_handle import db_handle
from analysis.Derivative import Derivative
from exchange_hook.exchange_interface import exchange
import time
import os.path
import json
import sys

current_path = os.path.abspath(os.path.dirname(__file__))
confPath = os.path.join(current_path, "./bot_params.json")
FakeTradePath = os.path.join(current_path,"./fake_records.db")
class trading_heart:
	def __init__(self, params):
		self.start_time = time.time()

		self.params=params
		self.ex=exchange("GDAX")

		#######################################
		#Initialization for FakeRecordDb
		self.FakeRecordDb() 
		#Determines last trade if sell or buy
		self.f_lasttrade = self.f_lastentry[0][7]
		self.f_lasttrade_price = self.f_lastentry[0][1]

		#######################################
		#######################################
		#Initialization for linear regression
		#   and exchange data
		#
		#fitWindow: sets linear regression to window 
		#           in seconds e.g., 60*60 is a 1 hour fit
		#xfit[-1]: latest time stamp
		self.fitWindow = 1*30*60
		self.slope, self.intercept, self.xfit = self.LinearFit(self.fitWindow)

		#######################################
		self.ticker_price = float(self.ex.auth_client.get_product_ticker('BTC-USD')['price'])
		self.price_target = self.ticker_price

		self.buy_limit = self.price_target * (1+self.slope) / float(params['aggression'])
		self.sel_limit = self.price_target * float(params['aggression'])

		bot_params_file = data_handle(confPath)
		tradeConf = bot_params_file.dictRead()
		tradeConf['price_target'] = self.price_target

		print("Buy Limit: ", '%.2f'% self.buy_limit)
		print("Sel Limit: ", '%.2f'% self.sel_limit)


	def patiently_trade(self, params):

		
		#Determines last trade if sell or buy
		self.FakeRecordDb() 
		self.f_lasttrade = self.f_lastentry[0][7]
		self.bank_btc = self.f_lastentry[0][6]
		self.bank_cash = self.f_lastentry[0][5]
		self.sequence = self.f_lastentry[0][0]

		# print()
		# print("  Ticker:  ", self.ticker_price)
		# print("  Target:  ", self.price_target)
		# print("Buy Limit: ", '%.2f'% self.buy_limit)
		# print("Sel Limit: ", '%.2f'% self.sel_limit)
		# print("Last Trade:", self.f_lasttrade)
		# print("BTC Bank:  ", '%.5f'% self.bank_btc)
		# print("Cash Bank: ", '%.2f'% self.bank_cash)
		if self.f_lasttrade == 'buy':
			#If last trade is a buy
			#execute a sell trade
			if self.sel_limit <= self.ticker_price:
				self.bank_btc = self.bank_btc-0.001
				self.bank_cash = self.bank_cash+0.001*self.ticker_price
				self.sequence = self.sequence +1
				self.f_lasttrade = 'sell'
				self.slope, self.intercept, self.xfit = self.LinearFit(self.fitWindow)
				self.buy_limit = self.ticker_price * (self.slope+1) / float(params['aggression'])
				self.FakeRecordTradesDb(self.sequence,self.ticker_price,0.001,time.time(),self.slope,self.bank_cash,self.bank_btc,'sell')
				print()
				print("-------  Sell executed  -------")
				print("BTC Bank:     ", '%.5f'% self.bank_btc)
				print("Cash Bank:    ", '%.2f'% self.bank_cash)
				print("BTC Price:    ", '%.2f'% self.ticker_price)
				print("New Buy Limit:", '%.2f'% self.buy_limit)

		if self.f_lasttrade == 'sell':
			#If last trade is a sell
			#execute a buy trade
			if self.buy_limit >= self.ticker_price:
				self.bank_btc = self.bank_btc+0.001
				self.bank_cash = self.bank_cash-0.001*self.ticker_price
				self.sequence = self.sequence +1
				self.f_lasttrade = 'buy'
				self.slope, self.intercept, self.xfit = self.LinearFit(self.fitWindow)
				self.sel_limit = self.ticker_price * (self.slope+1) / float(params['aggression'])
				self.FakeRecordTradesDb(self.sequence,self.ticker_price,0.001,time.time(),self.slope,self.bank_cash,self.bank_btc,'buy')
				print()
				print("-------  Buy executed  -------")
				print("BTC Bank:     ", '%.2f'% self.bank_btc)
				print("Cash Bank:    ", '%.2f'% self.bank_cash)
				print("BTC Price:    ", '%.2f'% self.ticker_price)
				print("New Sell Limit:", '%.2f'% self.sel_limit)


	def getLastTradeTimer(self):
		return time.time() - self.start_time

	def RecordTrades(self,trade_type,target,quantity):
		trade_dict_hold = {}
		trade_dict_hold['trade_type'] = trade_type
		trade_dict_hold['target']= target
		trade_dict_hold['quantity'] = quantity

		self.data_trades.fwrite(json.dumps(self.trade_dict_hold))        
	def FakeRecordTradesDb(self,sequence,price,size,ttime,slope,cash,btc,tradetype):
		data = {'sequence':sequence,'price':price,'size':size,'time':ttime,'slope':slope,'cash':cash,'btc':btc,'tradetype':tradetype}
		self.fdb.insert_trade(data)

	def FakeRecordDb(self):
		#Creates or instantiates the fake
		#database used for testing.
		columns = '(sequence integer, price real, size real, time real, slope real, cash real, btc real, tradetype char(4))'
		self.fdb = db_handle("fake_trades.db",'fake_trades',columns)
		self.FakeLastTrade()

	def FakeLastTrade(self):
		#Gets the most recent trade
		#denoted by the max sequence
		#value.
		self.fdb.c.execute('SELECT * from fake_trades WHERE sequence = (SELECT MAX(sequence) FROM fake_trades)')
		self.f_lastentry = self.fdb.c.fetchall()
		
	def LinearFit(self,fitWindow):
		#Returns the following linear fit data:
		#   Slope
		#   Intercept
		#   Most recent time value (this can be used to predict next value)
		self.pricev,self.sizev,self.timev = Derivative().ParseData()
		slope,intercept,xfit = Derivative().FitDataLinear(fitWindow,self.timev,self.pricev)
		return slope, intercept, xfit[-1]

def main():
	
	tradeConf = data_handle(confPath).dictRead()
	heart=trading_heart(tradeConf)
	
	#This is the Main InfiniteLoop
	while True:
		#Read Configuration Options
		try:

			tradeConf = data_handle(confPath).dictRead()
		except json.decoder.JSONDecodeError:
			print("bot_params.json format error")
			print("Using Values:")
			print("quantity", tradeConf['quantity'])
			print("buy aggression", tradeConf['buy aggression'])
			print("sell aggression",tradeConf['sell aggression'])
		
		#Execute Trading Heart
		try:
			heart.ticker_price = float(heart.ex.auth_client.get_product_ticker('BTC-USD')['price'])
			heart.patiently_trade(tradeConf)
		except:

			print("Error: ")
			main()
		
		#Pause
		time.sleep(8)

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("")
		print("Bye!")