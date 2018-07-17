import sqlite3

class db_handle(object):
	"""docstring for db_handle"""
	
	def __init__(self, db_name):
		self.db_name = db_name
		self.conn = sqlite3.connect(self.db_name, check_same_thread=False)  #brenton: This could cause issues in the future.
		self.c = self.conn.cursor()
		try:
			self.c.execute('''CREATE TABLE trades
				(sequence integer, price real, size real, stime real)''')
		except sqlite3.OperationalError:
			print(db_name, "Exists")
			print("Connecting to Database", self.db_name)
			print()

# This Functionality (formerly create_db()) was moved to __init__
	# def create_table(self):
	# 	try:
	# 		self.c.execute('''CREATE TABLE trades
	# 			(sequence integer, price real, size real, stime real)''')
	# 	except sqlite3.OperationalError:
	# 		print("Database Already Exists\n")
			
	def insert_trade(self, sequence, price, size, stime):

		trade = [(sequence, price, size, stime)]
		
		self.c.executemany('INSERT into trades VALUES (?,?,?,?)', trade)
		
		self.conn.commit()
		
	def read_trade(self): #brenton: this just reads the first line in the database

		self.c.execute('SELECT * FROM trades')
		
		return self.c.fetchone()
		
	def read_trade_from_seq(self, sequence):
		
		sql_seq = (sequence,)
		
		self.c.execute('SELECT * FROM trades WHERE sequence=?', sql_seq)
		
		return self.c.fetchone()
		
	def print_trades(self):
		
		print()
		print(" Dump Trades ")
		print("-------------")
		for row in self.c.execute('SELECT * FROM trades ORDER BY sequence'):
			print (row)
