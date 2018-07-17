import gdax
import data_handle

import db_handle

public_client = gdax.PublicClient()
#print(public_client.get_currencies())



# auth_client = gdax.AuthenticatedClient(
# 	key = "fb6aed7e161ebcef2455f0a127428db5", 
# 	b64secret = "vHE4hhjJcit8sy7/LloMEVsq3/S0N9ZHA+WdEl47dZTiVTZzj6r9vaz5vdelEfsqI8XVFEYWUAnu6KPLly6tNg==",
# 	passphrase = "slj3fdi6bxa",
# 	api_url="https://api-public.sandbox.gdax.com")

# historicData = public_client.get_product_historic_rates("BTC-USD",granularity=60)
# datastuff = data_handle.data_handle("btc_usd_data")
# datastuff.checkExist()
# print(historicData)
# print(datastuff.fileName)
# datastuff.fileName = "45"
# print(datastuff.fileName)
# datastuff.qwrite('a'.join(str(historicData) for e in historicData))

#check_sell = auth_client.sell(price='200.00',
#				size='0.01',
#				product_id='BTC-USD')
#auth_client.cancel_all(product_id='BTC-USD')
#print(auth_client.get_accounts()[0]['balance'])
#print(check_sell)
#print(auth_client.get_orders())
#print(auth_client.get_fills())


#################################################################db_handle Stuff

db = db_handle.db_handle("testdb2")

#Here are a bunch of Inserts to fill up the database

db.insert_trade(1, 9000, 1, 100)
db.insert_trade(2, 9000, 1, 100)
db.insert_trade(4, 9000, 1, 100)
db.insert_trade(5, 9000, 1, 100)
db.insert_trade(6, 9000, 1, 100)

print (db.read_trade_from_seq(6))

db.print_trades()

print("End of Test")
