import sqlite3

class db_handle(object):
	"""docstring for db_handle"""
	# def __init__(self):
	# 	#Hi

	def create_db(self,db_name):
		conn = sqlite3.connect(db_name)
		c = conn.cursor()
		c.execute('''CREATE TABLE trades
			(sequence integer, price real, size real, stime real)''')
			
	def insert_trade(self, db_name, sequence, price, size, stime):
		conn = sqlite3.connect(db_name)
		c = conn.cursor()
		
		trade = [(sequence, price, size, stime)]
		
		c.executemany('INSERT into trades VALUES (?,?,?,?)', trade)
		
		conn.commit()
		
	def read_trade(self, db_name, sequence): #brenton this just reads the first line in the database
		conn = sqlite3.connect(db_name)
		c = conn.cursor()
		
		c.execute('SELECT * FROM trades')
		
		return c.fetchone()
		
	def read_trade_from_seq(self, db_name, sequence):
		conn = sqlite3.connect(db_name)
		c = conn.cursor()
		
		sql_seq = (sequence,)
		
		c.execute('SELECT * FROM trades WHERE sequence=?', sql_seq)
		
		return c.fetchone()
		
	def print_trades(self, db_name):
		conn = sqlite3.connect(db_name)
		c = conn.cursor()
		for row in c.execute('SELECT * FROM trades ORDER BY sequence'):
			print (row)

	# def open_db(self, db_name)
	# 	conn = sqlite3.connect(db_name)
	# 	c = conn.cursor()