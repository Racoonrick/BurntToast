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

if __name__ == "__main__":
    import gdax
    import time

    class MyWebsocketClient(gdax.WebsocketClient):
        def __init__(self):
            gdax.WebsocketClient.__init__(self)
            self.PrintComma = False
            self.WebDict = {}
            self.trade_dict_hold={}
            
        def on_open(self):
            self.url = "wss://ws-feed.gdax.com/"
            self.products = ["BTC-USD"]
            self.message_count = 0
            print("Let's count the messages!")
            print(__name__)
            self.data_ws = dh("websocket_data")
            self.data_ws.fopen("a")
            self.data_raw = dh("websocket_raw")
            self.data_raw.fopen("a")
            self.data_trades = dh("websocket_trades")
            self.data_trades.fopen("a")

        def _listen(self):
            while not self.stop:
                try:
                    msg = json.loads(self.ws.recv())
                except Exception as e:
                    self.on_error(e)
                else:
                    self.on_message(msg)
                    self.RecordTrades(msg)
                    self.data_raw.fwrite(json.dumps(msg))
                    #self.UpdateBuySellRec(msg)
                    msg = {}
                    

        def on_message(self, msg):
            if 'price' in msg and 'type' in msg:
                print("Message type:", msg["type"], "\t@ %.3f" % float(msg["price"]))
            self.message_count += 1

        def on_close(self):
            self.data_ws.fwrite(json.dumps(self.WebDict))
            self.data_trades.fclose()
            self.data_ws.fclose()
            print("-- Goodbye! --")

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

        def RecordTrades(self,msg):
            if 'type' in msg and msg['type'] == 'match':
                self.trade_dict_hold['sequence']= int(msg['sequence'])
                self.trade_dict_hold['price'] = float(msg['price'])
                self.trade_dict_hold['size'] = float(msg['size'])
                self.trade_dict_hold['time'] = self.DateToSeconds(msg['time'])
                self.data_trades.fwrite(json.dumps(self.trade_dict_hold))

        def DateToSeconds(self,msg_time):
            utc_dt = datetime.strptime(msg_time, '%Y-%m-%dT%H:%M:%S.%fZ')
            timestamp = (utc_dt - datetime(1970, 1, 1)).total_seconds()
            return timestamp




    
    wsClient = MyWebsocketClient()
    wsClient.start()
    print(wsClient.url, wsClient.products)
    print("\nMessageCount =", "%i \n" % wsClient.message_count)
    time.sleep(10)
    time.sleep(3)

    wsClient.close()