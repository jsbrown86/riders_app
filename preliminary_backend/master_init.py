import sqlite3

conn = sqlite3.connect('master.db')
print ("Opened master database successfully")

conn.execute('CREATE TABLE mdb (uoid INT)')
print ("Table created successfully")
conn.close()
