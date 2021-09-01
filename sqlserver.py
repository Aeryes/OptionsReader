import sqlite3
from sqlite3 import Error
from datetime import datetime

class SQLServer:
	def __init__(self, path):
		self.connection = None
		self.path = path
		self.logfilename = datetime.today().strftime('%Y-%m-%d-%H-%M-%S') + "-SQLITE"

	def write_to_logs(self, msgtype):
		with open('logs/' + '.txt', 'a') as self.json_file:
				if msgtype == "connectionest":
					self.json_file.write("\nSQLite Connection Successful...")
				else:
					self.json_file.write(msgtype)

	def create_connection(self):
		try:
			self.connection = sqlite3.connect(self.path)
			self.write_to_logs("connectionest")
		except Error as e:
			self.write_to_logs("SQLite Connection Error: {}".format(e))

		return self.connection

	def create_table(self):
		print("TEST")
