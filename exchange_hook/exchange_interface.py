from data_handling.data_handle import data_handle as dh
import json
import gdax
import os

current_path = os.path.abspath(os.path.dirname(__file__))

def toptest(): #this exists to test normal functions (with no class)
	print ("test2")

class exchange:
	loginPath = os.path.join(current_path, "../../login.sandbox.json")
	loginData = dh(loginPath).dictRead()
	auth_client = None
	
	def __init__(self, exchangeName):
		if exchangeName=="GDAX":
			self.exchangeName="GDAX"
			exchange.auth_client = gdax.AuthenticatedClient(
				exchange.loginData['key'],
				exchange.loginData['b64secret'],
				exchange.loginData['passphrase'],
				exchange.loginData['api_url'])

	def accountInfo(self):
		print("TODO: Make accountInfo function")

	def printLoginInfo(self):
		if self.exchangeName == "GDAX":
			data = dh(exchange.loginPath).dictRead()
			print ("key: ", data['key'])
			print ("b64secret: ", data['b64secret'])
			print ("passphrase: ", data['passphrase'])
		else:
			print("Error: Exchange Not Found")
	
	def buy(self, price_param, size_param, product_id_param):
		if self.exchangeName == "GDAX":
			exchange.auth_client.buy(price = price_param,
				size = size_param, product_id = product_id_param)
			print('Buy Order Placed')
			print(' --- ')
			print('Price: ', price_param)
			print('Size: ', size_param)
			print('Product: ', product_id_param)
		else:
			print("Error: Exchange Not Found")

	def sell(self, price_param, size_param, product_id_param):
		if self.exchangeName == "GDAX":
			exchange.auth_client.sell(price = price_param,
				size = size_param, product_id = product_id_param)
			print('Sell Order Placed')
			print(' --- ')
			print('Price: ', price_param)
			print('Size: ', size_param)
			print('Product: ', product_id_param)
		else:
			print("Error: Exchange Not Found")

#this method isn't working
	def getOrders(self):
		if self.exchangeName == "GDAX":
			orders = exchange.auth_client.get_orders()
			print (json.dumps(orders, sort_keys=True, indent=4, separators=(',', ': ')))
			return orders
		else:
			print("Error: Exchange Not Found")
	
	def printBalances(self):
		if self.exchangeName == "GDAX":
			for i in self.auth_client.get_accounts():
				print(i['currency'], i['balance'])
		else:
			print("Error: Exchange Not Found")
	
	@staticmethod #this exists to test the behavior of static methods
	def test():
		print (exchange.loginData['key'])
		print (exchange.loginData['b64secret'])
		print (exchange.loginData['passphrase'])
