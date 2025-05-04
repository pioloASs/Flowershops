import sqlite3

conn = sqlite3.connect('employee.db')
cursor = conn.cursor()

# Create the users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        fullname TEXT,
        phone TEXT,
        email TEXT PRIMARY KEY,
        password TEXT
    )
''')

conn.commit()
conn.close()

print("Users table created successfully.")
