from data_handling.data_handle import data_handle
from exchange_hook.exchange_interface import exchange
import time
import os.path
import json

current_path = os.path.abspath(os.path.dirname(__file__))

class trading_heart:
    def __init__(self, params):
        self.params=params
        self.ex=exchange("GDAX")
        self.buytarget = 0.0
        self.seltarget = 0.0
        print("init")

    def trade(self, params):

        print("Buy Target: ", self.buytarget)
        print("Sel Target: ", self.seltarget, "\n")

        if self.ex.getOrders() == [[]]:  # Only place order if no open orders
            ticker_price = float(self.ex.auth_client.get_product_ticker('BTC-USD')['price'])
            
            self.buytarget = ticker_price + float(params['buy buffer'])
            self.seltarget = ticker_price * float(params['sell aggression'])

            self.buytarget_str ='%.2f'% self.buytarget
            self.seltarget_str ='%.2f'% self.seltarget

            self.ex.buy(self.buytarget_str, str(params['quantity']), 'BTC-USD')
            self.ex.sell(self.seltarget_str, str(params['quantity']), 'BTC-USD')
            

def main():
    confPath = os.path.join(current_path, "./bot_params.json")
    tradeConf = data_handle(confPath).dictRead()
    heart=trading_heart(tradeConf)
 	
	#This is the Main InfiniteLoop
    while True:
        #Read Configuration Options
        try:
            tradeConf = data_handle(confPath).dictRead()
        except json.decoder.JSONDecodeError:
            print("bot_params.json format error")
            print("Using Values:")
            print("quantity", tradeConf['quantity'])
            print("buy buffer", tradeConf['buy buffer'])
            print("sell aggression",tradeConf['sell aggression'])
        
        #Execute Trading Heart
        heart.trade(tradeConf)
        
        #Pause
        time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("")
        print("Bye!")