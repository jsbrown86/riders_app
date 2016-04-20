import sqlite3

conn = sqlite3.connect('master.db')
print ("Opened master database successfully")

conn.execute('CREATE TABLE mdb (time TEXT, name TEXT, phone TEXT, uo_id INT, to_addr TEXT, from_addr TEXT, riders TEXT, active TEXT, comments TEXT)')
print ("Table created successfully")
conn.close()
