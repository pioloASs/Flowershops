import sqlite3

emp='employee.db'
con = sqlite3.connect(emp)

c = con.cursor()
c.execute(""" INSERT INTO tao(flo,col, arr) VALUES
    ('Iris','Violet','Boquet'),
     ('Daisy','White','Boquet'),
     ('Lily','Pink','Boquet')
""")
con.commit()
con.close()