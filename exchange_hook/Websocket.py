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
        def on_open(self):
            self.url = "wss://ws-feed.gdax.com/"
            self.products = ["BTC-USD", "ETH-USD"]
            self.message_count = 0
            print("Let's count the messages!")
            print(__name__)
            self.data_ws = dh("websocket_data")
            self.data_ws.fopen("a")

        def _listen(self):
            while not self.stop:
                try:
                    msg = json.loads(self.ws.recv())
                except Exception as e:
                    self.on_error(e)
                else:
                    self.on_message(msg)
                    self.data_ws.fwrite(json.dumps(msg)+"\n")

        def on_message(self, msg):
            if 'price' in msg and 'type' in msg:
                print("Message type:", msg["type"], "\t@ %.3f" % float(msg["price"]))
            self.message_count += 1
            self.msg2 = msg


        # def return_message(self):
        #     return self.msg2

        def on_close(self):
            
            self.data_ws.fclose()
            print("-- Goodbye! --")

    
    wsClient = MyWebsocketClient()
    wsClient.start()
    print(wsClient.url, wsClient.products)
    # Do some logic with the data
    #while wsClient.message_count < 500:
    print("hi")
    print("\nMessageCount =", "%i \n" % wsClient.message_count)
    time.sleep(1)
    #mout = wsClient.return_message()

    #print(mout)
    time.sleep(2)

    wsClient.close()