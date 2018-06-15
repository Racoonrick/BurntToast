from data_handling.data_handle import data_handle as dh
import json
import gdax

def toptest():
	print ("test2")

class exchange:
	loginPath="login.json" #Copy the JSON file to the directory you execute your program from
	loginData = dh(loginPath).dictRead()
	auth_client = gdax.AuthenticatedClient(loginData['key'], 
		loginData['b64secret'], loginData['passphrase'])
	
	def __init__(self, exchangeName):
		self.exchangeName="GDAX"
	# 	exchange.loginData = dh(loginPath).dictRead()
	# 	exchange.auth_client = gdax.AuthenticatedClient(exchange.loginData['key'], 
	# 	exchange.loginData['b64secret'], exchange.loginData['passphrase'])
	# 	#self.exchangeName = exchangeName

	def accountInfo(self):
		if self.exchangeName == "GDAX":
			data = dh(exchange.loginPath).dictRead()
			print (data['key'])
			print (data['b64secret'])
			print (data['passphrase'])
		else:
			print("Error: Exchange Not Found")
	
	def buy(self, price, size, product_id):
		if self.exchangeName == "GDAX":
			exchange.auth_client.buy(price = price,
			size = size, product_id = product_id)
			print('Buy Order Placed')
			print(' --- ')
			print('price: ', price)
			print('size: ', size)
			print('productId: ', product_id)
		else:
			print("Error: Exchange Not Found")
			
	def getOrders(self):
		if self.exchangeName == "GDAX":
			orders = exchange.auth_client.get_orders()
			print (json.dumps(orders, sort_keys=True, indent=4, separators=(',', ': ')))
			return orders
		else:
			print("Error: Exchange Not Found")
	
	def printBalances(self):
		if self.exchangeName == "GDAX":
			for i in exchange.auth_client.get_accounts():
				# print(i['currency'], i['balance'])
				print(i)
		else:
			print("Error: Exchange Not Found")
	
	@staticmethod
	def test():
		print (exchange.loginData['key'])
		print (exchange.loginData['b64secret'])
		print (exchange.loginData['passphrase'])

	# def getBalance(self):
	# 	if exchangeName =="GDAX":
			
	# 	return