from data_handling.data_handle import data_handle as dh
import json
#import gdax

print ("test1")

def toptest():
	print ("test2")

class exchange:
	exchangeName="GDAX"
	loginPath="login.json" #Copy the JSON file to the directory you execute your program from
	# def __init__(self):
		#self.exchangeName = exchangeName

	def accountInfo(self):
		if exchange.exchangeName == "GDAX":
			data = dh(exchange.loginPath).dictRead()
			print (data['key'])
			print (data['b64secret'])
			print (data['passphrase'])
		else:
			return {}
	
	@staticmethod
	def test():
		print ("test4")

	# def getBalance(self):
	# 	if exchangeName =="GDAX":
			
	# 	return