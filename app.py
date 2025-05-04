from flask import Flask, render_template, url_for, request, redirect
import sqlite3

emp = 'employee.db'
app = Flask(__name__)


def init_orders_table():
    conn = sqlite3.connect(emp)
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

def get_orders_from_db():
    conn = sqlite3.connect(emp)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    conn.close()
    return orders

def employee_data():
    con = sqlite3.connect(emp)
    c = con.cursor()
    c.execute("SELECT * FROM tao")
    em = c.fetchall()
    con.commit()
    con.close()
    return em

def get_user(email):
    conn = sqlite3.connect(emp)
    cursor = conn.cursor()
    cursor.execute("SELECT email, password FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {'email': row[0], 'password': row[1]}
    return None

@app.route('/admin')
def admin_no():
    data = get_orders_from_db()
    total_orders = len(data)
    total_revenue = sum(order[3] * 200 for order in data)  # assuming quantity * 200
    total_users = len(set(order[1] for order in data))

    return render_template('admin.html', data=data,
                           total_orders=total_orders,
                           total_revenue=total_revenue,
                           total_users=total_users)
@app.route('/edit/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    conn = sqlite3.connect(emp)
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        flower = request.form['flower']
        quantity = int(request.form['quantity'])

        cursor.execute("UPDATE orders SET name = ?, flower_type = ?, quantity = ? WHERE id = ?",
                       (name, flower, quantity, order_id))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_no'))

    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()
    conn.close()

    return render_template('edit_order.html', order=order)

@app.route('/submit_order', methods=['POST'])
def submit_order():
    name = request.form['flower']
    flower_type = request.form['color']
    quantity = request.form['arrangement']

    conn = sqlite3.connect(emp)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (name, flower_type, quantity) VALUES (?, ?, ?)",
        (name, flower_type, int(quantity))
    )
    conn.commit()
    conn.close()
    return redirect(url_for('admin_no'))

@app.route('/')
def log_in():
    data = employee_data()
    return render_template("login.html", data=data)

@app.route('/about')
def about_us():
    data = employee_data()
    return render_template("about.html", data=data)

@app.route('/order')
def order_here():
    data = employee_data()
    return render_template("order.html", data=data)

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = get_user(email)
    if user and user['password'] == password:
        return redirect(url_for('home'))
    data = employee_data()
    error = "Invalid email or password."
    return render_template("login.html", data=data, error=error)

@app.route('/register', methods=['POST'])
def register():
    fullname = request.form['fullname']
    phone = request.form['phone']
    email = request.form['email']
    password = request.form['password']

    if get_user(email):
        data = employee_data()
        error = "User already exists."
        return render_template("login.html", data=data, error=error)

    conn = sqlite3.connect(emp)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (fullname, phone, email, password) VALUES (?, ?, ?, ?)",
                   (fullname, phone, email, password))
    conn.commit()
    conn.close()
    return redirect(url_for('log_in'))

@app.route('/home')
def home():
    data = employee_data()
    return render_template("index.html", data=data)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'GET':
        return render_template("adding.html")
    else:
        e_details = [
            request.form['flower'],
            request.form['color'],
            request.form['arrangement']
        ]
        adding(e_details)
        return render_template('adding.html')

def adding(e_details):
    con = sqlite3.connect(emp)
    c = con.cursor()
    sql_string = 'INSERT INTO tao(flo, col, arr) VALUES (?, ?, ?)'
    c.execute(sql_string, e_details)
    con.commit()
    con.close()

if __name__ == '__main__':
    init_orders_table()
    app.run(debug=True)
