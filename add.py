def init_orders_table():
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            flower_type TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM orders")
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO orders (name, flower_type, quantity)
            VALUES (?, ?, ?)
        ''', [
            ("Alice", "Roses", 3),
            ("Bob", "Tulips", 5),
            ("Carol", "Daisies", 2)
        ])
    conn.commit()
    conn.close()
