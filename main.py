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
        self.data_trades = data_handle("trades_record")
        self.data_trades.fopen("a")

    def trade(self, params):

        print("Buy Target: ", self.buytarget)
        print("Sel Target: ", self.seltarget, "\n")

        if self.ex.getOrders() == [[]]:  # Only place order if no open orders
            #Opens data_trades for write
            self.data_trades.fopen("a")

            ticker_price = float(self.ex.auth_client.get_product_ticker('BTC-USD')['price'])
            
            self.buytarget = ticker_price + float(params['buy buffer'])
            self.seltarget = ticker_price * float(params['sell aggression'])

            self.buytarget_str ='%.2f'% self.buytarget
            self.seltarget_str ='%.2f'% self.seltarget

            self.ex.buy(self.buytarget_str, str(params['quantity']), 'BTC-USD')
            self.RecordTrades("buy",self.buytarget_str,str(params['quantity']))
            self.ex.sell(self.seltarget_str, str(params['quantity']), 'BTC-USD')
            self.RecordTrades("sell",self.seltarget_str,str(params['quantity']))

            #Closes file for recording trading data
            self.data_trades.fclose()

    def RecordTrades(self,trade_type,target,quantity):
        self.trade_dict_hold = {}
        self.trade_dict_hold['trade_type'] = trade_type
        self.trade_dict_hold['target']= target
        self.trade_dict_hold['quantity'] = quantity
        self.data_trades.fwrite(json.dumps(self.trade_dict_hold))        

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