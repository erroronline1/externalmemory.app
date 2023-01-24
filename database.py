# -*- coding: utf-8 -*-
import sqlite3

class DataBase():
	tableFields = {
		"DATA": ["ID", "MEMO", "RATING"],
		"SETTING": ["KEY", "VALUE"]
	}
	status = ""
	def __init__(self, db):
		# tries to establish connection, creates on fail.
		try:
			self.connection = sqlite3.connect(db)
			c = self.connection.cursor()
			c.execute(f'''
				CREATE TABLE IF NOT EXISTS DATA
				({self.tableFields["DATA"][0]} TEXT PRIMARY KEY NOT NULL,
				{self.tableFields["DATA"][1]} TEXT,
				{self.tableFields["DATA"][2]} INTEGER);''')
			c.execute(f'''
				CREATE TABLE IF NOT EXISTS SETTING
				({self.tableFields["SETTING"][0]} TINYTEXT UNIQUE,
				{self.tableFields["SETTING"][1]} TINYTEXT);''')
			self.connection.commit()
		except Exception as error:
			self.status +=f" {error} {db}"

	def __del__(self):
		self.connection.close()

	def write(self, table="", key_value={}, where={}):
		condition, values, updates = [], [], []
		for key in where:
			condition.append(f"{self.sanitize(key, False)}={self.sanitize(where[key])}")
		for column in self.tableFields[table]:
			if column in key_value:
				values.append(f"{self.sanitize(key_value[column])}")
				updates.append(f"{column}={self.sanitize(key_value[column])}")
			else:
				values.append("NULL")
		# try to update exsting
		if len(condition):
			self.connection.execute(f"UPDATE {table} SET {', '.join(updates)} WHERE {' AND '.join(condition)};")
		# otherwise insert
		self.connection.execute(f"INSERT OR IGNORE INTO {table} ({', '.join(self.tableFields[table])}) VALUES ({', '.join(values)});")
		self.connection.commit()
		return True

	def read(self, fields = [], table = "", where = {}):
		condition, fields = [], [self.sanitize(field, False) for field in fields] if fields else "*"
		for key in where:
			condition.append(f"{self.sanitize(key, False)}={self.sanitize(where[key])}")
		cursor = self.connection.cursor()
		cursor.execute(f"SELECT {' AND '.join(fields)} FROM {table} {('WHERE ' + ' AND '.join(condition)) if len(condition) else ''};")
		result = cursor.fetchall()
		if result is not None:
			return result
		return False

	def delete(self, table = "", where = {}):
		condition= []
		for key in where:
			condition.append(f"{self.sanitize(key, False)}={self.sanitize(where[key])}")
		if len(condition):
			self.connection.execute(f"DELETE FROM {table} WHERE {' AND '.join(condition)};")
		self.connection.commit()
		return True

	def sanitize(self, value = "", quotes = True):
		# sanitary strings to concatenate to sql queries.
		# if not quotes it probbly is a column key
		if type(value)==str and value != "NULL":
			if value.strip()=="":
				return "NULL"
			return value.replace('\'','\'\'') if not quotes else "'" + value.replace('\'','\'\'') + "'"
		return value

	def clear(self, tables=[]):
		# reset database
		for table in tables:
			self.connection.executescript(f"DELETE FROM {table}; VACUUM;")
		self.connection.commit()
		return True