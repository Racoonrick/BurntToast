import data_handle
import json

class exchange:
	#def __init__(self,exchangeName):
		#self.exchangeName = exchangeName

	def accountInfo(infoPath,exchangeName="GDAX"):
		if exchangeName == "GDAX":
			return data_handle.data_handle(infoPath).dictRead()
		else:
			return {}

	