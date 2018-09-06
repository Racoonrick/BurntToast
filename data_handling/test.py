import gdax
import data_handle
from data_handling.db_handle import db_handle as dbh
import db_handle

from exchange_hook.exchange_interface import exchange

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
# test_str = '(sequence integer, price real, size real, time real)'
# db = db_handle.db_handle("fake_trades",'trades',test_str)

# #Here are a bunch of Inserts to fill up the database
# #self.trade_dict_hold
# data = {'time':1532723000,'price':8240,'size':1,'sequence':100}
# db.insert_trade(data)
# data = {'time':1532728000,'price':8200,'size':1,'sequence':101}
# db.insert_trade(data)
# data = {'time':1532730350,'price':8180,'size':1,'sequence':102}
# db.insert_trade(data)
# data = {'time':1532733400,'price':8140,'size':1,'sequence':103}
# db.insert_trade(data)
# data = {'time':1532733450,'price':8150,'size':1,'sequence':104}
# db.insert_trade(data)

# print (db.read_trade_from_seq(6))

# db.print_trades()

# print([description[0] for description in db.c.description])
# print("End of Test")
# array1 = []
# i = 0
# d = {'l':0,'a':1,'b':2,'c':3}
# for keys in d.keys():
# 	array1.insert(i,d[keys])
# 	i=i+1
# print(array1)
################################################################Exchange Stuff

# ex=exchange("GDAX")

# ex.getOrders()

# # ex.buy("3000.1", ".002", 'BTC-USD')

# ex.auth_client.cancel_all()

# # if ex.getOrders() == [[]]:
# # 	print("Yes")
# # else:
# # 	print("no")

#################################################################Sorting Data Base Ex

# test_str = '(sequence integer, price real, size real, time real)'

# db = db_handle.db_handle("websocket_trades_db",'trades',test_str)
# db.conn.execute("SELECT * FROM trades ORDER BY sequence ASC")
# db.print_trades()

db_path ="C:/Users/Ricky/Documents/Work/BurntToast/fake_trades.db"
tname = 'fake_trades'
tcolumns = '(sequence integer, price real, size real, time real, slope real, cash real, btc real, tradetype char(4))'
algo_dbh = dbh(db_path,tname,tcolumns)
algo_dbh.c.execute('SELECT * FROM fake_trades')
data = algo_dbh.c.fetchall()
print(data)