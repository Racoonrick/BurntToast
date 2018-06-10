import gdax
import data_handle

public_client = gdax.PublicClient()
#print(public_client.get_currencies())



auth_client = gdax.AuthenticatedClient(
	key = "fb6aed7e161ebcef2455f0a127428db5", 
	b64secret = "vHE4hhjJcit8sy7/LloMEVsq3/S0N9ZHA+WdEl47dZTiVTZzj6r9vaz5vdelEfsqI8XVFEYWUAnu6KPLly6tNg==",
	passphrase = "slj3fdi6bxa",
	api_url="https://api-public.sandbox.gdax.com")

historicData = public_client.get_product_historic_rates("BTC-USD",granularity=60)
datastuff = data_handle.data_handle("btc_usd_data")
datastuff.checkExist()
print(historicData)
datastuff.qwrite('a'.join(str(historicData) for e in historicData))

#check_sell = auth_client.sell(price='200.00',
#				size='0.01',
#				product_id='BTC-USD')
#auth_client.cancel_all(product_id='BTC-USD')
#print(auth_client.get_accounts()[0]['balance'])
#print(check_sell)
#print(auth_client.get_orders())
#print(auth_client.get_fills())
