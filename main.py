from data_handling.data_handle import data_handle
from exchange_hook.exchange_interface import exchange
import time
import os.path
import json

current_path = os.path.abspath(os.path.dirname(__file__))
confPath = os.path.join(current_path, "./bot_params.json")

class trading_heart:
    def __init__(self, params):
        self.start_time = time.time()

        self.params=params
        self.ex=exchange("GDAX")
        # self.ex.getOrders()
        # self.ex.auth_client.cancel_all()

        ticker_price = float(self.ex.auth_client.get_product_ticker('LTC-USD')['price'])
        self.price_target = ticker_price
        self.buy_limit = self.price_target / float(params['aggression'])
        self.sel_limit = self.price_target * float(params['aggression'])
        self.buyorsell = "buy"

        self.data_trades = data_handle("trades_record")
        self.data_trades.fopen("a")

        bot_params_file = data_handle(confPath)
        tradeConf = bot_params_file.dictRead()
        tradeConf['price_target'] = self.price_target
        bot_params_file.fopen("w")
        bot_params_file.fwrite(json.dumps(tradeConf, indent=4))
        bot_params_file.fclose()

    def patiently_trade(self, params):

        ticker_price = float(self.ex.auth_client.get_product_ticker('LTC-USD')['price'])

        print("  Ticker:  ", ticker_price)
        print("  Target:  ", self.price_target)
        print("Buy Limit: ", '%.2f'% self.buy_limit)
        print("Sel Limit: ", '%.2f'% self.sel_limit)

        if self.ex.getOrders() == [[]]:  # Only place order if no open orders

            #Opens data_trades for write
            self.data_trades.fopen("a")

            self.buytarget = self.price_target / float(params['aggression'])
            self.seltarget = self.price_target * float(params['aggression'])

            self.buy_limit_str ='%.2f'% self.buy_limit
            self.sel_limit_str ='%.2f'% self.sel_limit

            if self.buyorsell == "buy":
                self.ex.buy(self.buy_limit_str, str(params['quantity']), 'LTC-USD')
                self.RecordTrades("buy",self.buy_limit_str,str(params['quantity']))
                self.buyorsell="sell"

            if self.buyorsell == "sell":
                self.ex.sell(self.sel_limit_str, str(params['quantity']), 'LTC-USD')
                self.RecordTrades("sell",self.sel_limit_str,str(params['quantity']))
                self.buyorsell="buy"

            #Reset Trade Timer
            self.start_time = time.time()

            #Closes file for recording trading data
            self.data_trades.fclose()
        else:
            if self.buyorsell == "sell":
                print("Open Order: Buy")
            elif self.buyorsell == "buy":
                print("Open Order: Sell")
            else:
                print("Error with Open Orders")
            print()

    #Time since the last order was placed (in seconds)
    def getLastTradeTimer(self):
        return time.time() - self.start_time

    def RecordTrades(self,trade_type,target,quantity):
        self.trade_dict_hold = {}
        self.trade_dict_hold['trade_type'] = trade_type
        self.trade_dict_hold['target']= target
        self.trade_dict_hold['quantity'] = quantity
        self.data_trades.fwrite(json.dumps(self.trade_dict_hold))        

def main():
    
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
        heart.patiently_trade(tradeConf)
        
        #Pause
        time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("")
        print("Bye!")