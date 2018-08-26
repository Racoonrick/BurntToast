from data_handling.data_handle import data_handle
from data_handling.db_handle import db_handle
from exchange_hook.exchange_interface import exchange
import time
import os.path
import json

columns = '(sequence integer, price real, size real, time real, slope real, cash real, btc real, tradetype char(4))'
fdb = db_handle("fake_trades.db",'fake_trades',columns)
#data = {'sequence':0,'price':6014,'size':1,'time':time.time(),'slope':0.001,'cash':600.00,'btc':0.100,'tradetype':'buy'}
#fdb.insert_trade(data)
fdb.c.execute('SELECT * from fake_trades WHERE sequence = (SELECT MAX(sequence) FROM fake_trades)')
fdb.c.execute('SELECT * from fake_trades')
fdata = fdb.c.fetchall()
print(fdata)
print()
#print(fdata[11])
fitWindow = 1*60*60
