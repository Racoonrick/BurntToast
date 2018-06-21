from data_handling.data_handle import data_handle
from exchange_hook.exchange_interface import exchange
import time
import os.path

current_path = os.path.abspath(os.path.dirname(__file__))

class trading_heart:
    def __init__(self, params):
        self.params=params
        self.ex=exchange("GDAX")
        print("init")

    def trade(self, params):
        print("Trade")
        print("Trade Param 2: ", params['param2'])  #Proof that Parameters are read from bot_params.json
        #self.ex.printBalances()                     #Proof that Trading Heart is interacting with GDAX

def main():
    confPath = os.path.join(current_path, "./bot_params.json")
    tradeConf = data_handle(confPath).dictRead()
    heart=trading_heart(tradeConf)
 	
	#This is the Main InfiniteLoop
    while True:
        #Read Configuration Options
        tradeConf = data_handle(confPath).dictRead()
        # print("Trade Param 1: ", tradeConf['param1']) #Param Read Test
        
        #Execute Trading Heart
        heart.trade(tradeConf)
        
        #Pause
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("")
        print("Bye!")