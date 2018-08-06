#
# gdax/WebsocketClient.py
# Daniel Paquin
#
# Template object to receive messages from the gdax Websocket Feed

from __future__ import print_function
import json

from gdax      import WebsocketClient
from threading import Thread
from datetime import datetime
from websocket import create_connection, WebSocketConnectionClosedException
from data_handling.data_handle import data_handle as dh
from data_handling.db_handle import db_handle as dbh
import gdax
import time
import os


class MyWebsocketClient(gdax.WebsocketClient):
    def __init__(self):
        self.clear = lambda: os.system('cls')
        gdax.WebsocketClient.__init__(self)
        self.PrintComma = False
        self.WebDict = {}
        
    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/"
        self.products = ["BTC-USD"]
        self.message_count = 0
        print("Let's count the messages!")
        print(__name__)
        #
        self.data_ws = dh("websocket_data")
        self.data_ws.fopen("a")

        self.data_raw = dh("websocket_raw")
        self.data_raw.fopen("a")

        self.data_trades = dh("websocket_trades")
        self.data_trades.fopen("a")

        
        tname = 'trades'
        tcolumns = '(sequence integer, price real, size real, time real)'
        self.database_trades = dbh("websocket_trades_db",tname,tcolumns)

    def _listen(self):
        global msg 
        while not self.stop:
            try:
                msg = json.loads(self.ws.recv())
            except Exception as e:
                self.on_error(e)
                #Added these lines to restart the websocket in the event of an error
                #This may not work
                self.close()
                self.start()
            else:
                self.on_message(msg)
                #self.RecordTrades(msg)
                #self.data_raw.fwrite(json.dumps(msg))
                #self.UpdateBuySellRec(msg)
                
                self.RecordTrades_db(msg)
                
                msg = {}
                

    def on_message(self, msg):
        # if 'price' in msg and 'type' in msg:
        #     print("Message type:", msg["type"], "\t@ %.3f" % float(msg["price"]))
        self.message_count += 1

    def on_close(self):
        self.data_ws.fwrite(json.dumps(self.WebDict))
        self.data_trades.fclose()
        self.data_ws.fclose()
        print("-- Goodbye! --")
    def on_error(self, e):
        print(e)
        return
    def UpdateBuySellRec(self,msg):
        if 'order_id' in msg:
            if 'reason' in msg:
                if ((msg['reason'] == 'canceled') or (msg['reason'] == 'filled')) and (msg['order_id'] in self.WebDict):
                    del self.WebDict[msg['order_id']]
            else:
                order_id = msg['order_id']
                #Delete removes from dictionary and all reference dictionaries
                del msg['order_id']
                self.WebDict[order_id] = msg

    def MsgToDict(self,msg):
        trade_dict_hold = {}
        trade_dict_hold['sequence']= int(msg['sequence'])
        trade_dict_hold['price'] = float(msg['price'])
        trade_dict_hold['size'] = float(msg['size'])
        trade_dict_hold['time'] = self.DateToSeconds(msg['time'])
        return trade_dict_hold

    def RecordTrades(self,msg):
        if 'type' in msg and msg['type'] == 'match':
            trade_data = self.MsgToDict(msg)
            self.data_trades.fwrite(json.dumps(trade_data))
            
    def RecordTrades_db(self,msg):
        if 'type' in msg and msg['type'] == 'match':
            trade_data = self.MsgToDict(msg)
            self.database_trades.insert_trade(trade_data)
            self.clear()
            print("Trade: "+msg['price']+" Time: "+str(datetime.now()))

    def DateToSeconds(self,msg_time):
        utc_dt = datetime.strptime(msg_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        timestamp = (utc_dt - datetime(1970, 1, 1)).total_seconds()
        return timestamp



if __name__ == "__main__":

    wsClient = MyWebsocketClient()
    wsClient.start()
    print(wsClient.url, wsClient.products)
    i = 0
    while True:
        i = 1


