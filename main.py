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
        self.buyorsell = "buy"
        self.pricetarget = 0.0
        print("init")

    def trade(self, params):
        
        ticker_price = float(self.ex.auth_client.get_product_ticker('BTC-USD')['price'])
        self.pricetarget = ticker_price * float(params['buy aggression'])
        
        print("Ticker Price: ", ticker_price)
        print("Buy/Sell: ", self.buyorsell)
        print("Price Target: ", self.pricetarget, "\n")
        
        if self.ex.getOrders() == [[]]:  # Only place order if no open orders
            if self.buyorsell == "buy":
                self.ex.buy(ticker_price, params['quantity'], 'BTC-USD')
                #do a market buy
                self.pricetarget *= float(params['sell aggression'])
                self.buyorsell = "sell"  # Alternate between Buy & Sell
                return
            if self.buyorsell == "sell":
                if ticker_price > self.pricetarget:
                    self.ex.sell(self.pricetarget, params['quantity'], 'BTC-USD')
                    self.buyorsell = "buy"  # Alternate between Buy & Sell
                return

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
            print("buy aggression", tradeConf['buy aggression'])
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