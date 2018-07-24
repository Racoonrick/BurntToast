import sqlite3
import numpy as np
class db_handle(object):
	"""docstring for db_handle"""
	
	def __init__(self, db_name,table_name,table_columns):
		self.db_name = db_name
		self.conn = sqlite3.connect(self.db_name, check_same_thread=False)  #brenton: This could cause issues in the future.
		self.c = self.conn.cursor()
		self.data_sql = []
		self.table_name = table_name
		table_format = self.TableFormat(table_name,table_columns)
		try:
			#
			#Example table format:
			#            TABLE_NAME  COLUMN 0   	COLUMN 1	COLUMN 2	COLUMN 3
			#					|		|		 		|		   |           |
			#'''CREATE TABLE trades (sequence integer, price real, size real, stime real)'''
			#
			self.c.execute(table_format)
		except sqlite3.OperationalError:
			print(db_name, "Exists")
			print("Connecting to Database", self.db_name)
			print()

		self.key_array = self.GetColumnName()

	def TableFormat(self,table_name,table_columns):
		#Ricky:
		#	Formats the sql table creation string
		table_format = '''CREATE TABLE '''+table_name+table_columns
		return table_format

	def GetColumnName(self):
		#Ricky:
		#	Returns array of keys 
		#		This is to ensure that we are only putting data in 
		#		that matches the database columns
		cursor = self.conn.execute('select * from '+self.table_name)
		keys = list(map(lambda x: x[0], cursor.description))

		# Ricky:
		#	This generates the correct number of 
		#	question marks for the database.
		QuestionMarksStart = "("
		for i in keys:
			QuestionMarksStart = QuestionMarksStart +"?,"

		QuestionMarksStart = QuestionMarksStart[:-1]+")"
		self.QuestionMarks = QuestionMarksStart

		return keys	

	def insert_trade(self, data):
		try:
			#	Ricky:
			#		First we conver the dictionary to a list in order with it's keys
			#		Then we convert the list to a tuple for insertion
			#		Finally we convert it back to a list for SQL
			data_list = [data[key_v[:]] for key_v in self.key_array]
			data_t = tuple(data_list)
			self.data_sql = [data_t]

		except KeyError:
			print("Error: Data inserted does not match database columns. Check table_format")
		
		#Row insert size determined on initialization
		execute_str = 'INSERT into ' + self.table_name + ' VALUES '+self.QuestionMarks
		self.c.executemany(execute_str, self.data_sql)
		
		self.conn.commit()
		
	def read_trade(self): #brenton: this just reads the first line in the database

		self.c.execute('SELECT * FROM '+self.table_name)
		
		return self.c.fetchone()
		
	def read_trade_from_seq(self, sequence):
		
		sql_seq = (sequence,)
		
		self.c.execute('SELECT * FROM ' + self.table_name +' WHERE sequence=?', sql_seq)
		
		return self.c.fetchone()
		
	def print_trades(self):
		
		print()
		print(" Dump Data ")
		print("-------------")
		for row in self.c.execute('SELECT * FROM '+self.table_name+' ORDER BY sequence'):
			print (row)
