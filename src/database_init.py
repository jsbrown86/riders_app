import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE requests (time TEXT, name TEXT, phone TEXT, uo_id INT PRIMARY KEY, to_addr TEXT, from_addr TEXT, riders TEXT, active TEXT, comments TEXT)')
print ("Table created successfully")
conn.close()
