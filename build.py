import sqlite3

emp= 'employee.db'
con= sqlite3.connect(emp)

c = con.cursor()
c.execute(""" CREATE TABLE tao
   ( id INTEGER PRIMARY KEY AUTOINCREMENT,
    flo TEXT,
    col TEXT,
    arr TEXT)

""")
con.commit()
con.close()