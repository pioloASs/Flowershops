import sqlite3

emp='employee.db'
con = sqlite3.connect(emp)

c = con.cursor()
c.execute(""" SELECT * FROM tao
""")
records=c.fetchall()
for rec in records:
    print (rec)
con.commit()
con.close()