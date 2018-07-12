import sqlite3

class db_handle(object):
	"""docstring for db_handle"""
	def __init__(self):
		#Hi

	def create_db(self,db_name):
		conn = sqlite3.connect(db_name)
		c = conn.cursor()
		c.execute('''CREATE TABLE trades
             (sequence real, price real, size real, stime time)''')
