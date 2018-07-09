#
# gdax/WebsocketClient.py
# Daniel Paquin
#
# Template object to receive messages from the gdax Websocket Feed

from __future__ import print_function
import json

from gdax      import WebsocketClient
from threading import Thread
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

        def _listen(self):
            while not self.stop:
                try:
                    msg = json.loads(self.ws.recv())
                except Exception as e:
                    self.on_error(e)
                else:
                    self.on_message(msg)
                    self.data_raw.fwrite(json.dumps(msg))
                    self.UpdateBuySellRec(msg)
                    msg = {}
                    

        def on_message(self, msg):
            if 'price' in msg and 'type' in msg:
                print("Message type:", msg["type"], "\t@ %.3f" % float(msg["price"]))
            self.message_count += 1

        def on_close(self):
            self.data_ws.fwrite(json.dumps(self.WebDict))
            
            self.data_ws.fclose()
            print("-- Goodbye! --")

        def UpdateBuySellRec(self,msg):
            if 'order_id' in msg:
                if 'reason' in msg:
                    if (msg['reason'] == 'canceled') and (msg['order_id'] in self.WebDict):
                        print("deleted")
                        del self.WebDict[msg['order_id']]
                else:
                    order_id = msg['order_id']
                    #Delete removes from dictionary and all reference dictionaries
                    del msg['order_id']
                    self.WebDict[order_id] = msg


    
    wsClient = MyWebsocketClient()
    wsClient.start()
    print(wsClient.url, wsClient.products)
    print("\nMessageCount =", "%i \n" % wsClient.message_count)
    time.sleep(60)
    #mout = wsClient.return_message()

    #print(mout)
    time.sleep(3)

    wsClient.close()