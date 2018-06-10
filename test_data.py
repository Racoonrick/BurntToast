import data_handle

test = data_handle.data_handle("btc_usd_data")
testdict = {"age":32,"fart":32,"test":"tru"}
test.dictWrite(testdict)
accnt = data_handle.data_handle("C:/Users/Ricky/Documents/Work/gdaxsb_api_key.txt")
info = accnt.dictRead()
print(info["passphrase"])