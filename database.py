import sqlite3
from datetime import datetime

def create_tables():
    conn = sqlite3.connect('schema.db')
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                    (username TEXT PRIMARY KEY, 
                     password TEXT NOT NULL)''')
    
    # Invoices Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS invoices 
                    (invoice_id TEXT PRIMARY KEY,
                     username TEXT,
                     total_amount REAL,
                     discount REAL,
                     timestamp TEXT,
                     FOREIGN KEY(username) REFERENCES users(username))''')
    
    # Cart Items Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS cart_items 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT,
                     product_name TEXT,
                     price REAL,
                     quantity TEXT,
                     category TEXT,
                     FOREIGN KEY(username) REFERENCES users(username))''')
    
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect('schema.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def check_user(username, password):
    conn = sqlite3.connect('schema.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def save_invoice(username, total_amount, discount, items):
    conn = sqlite3.connect('schema.db')
    cursor = conn.cursor()
    
    # Generate invoice ID
    timestamp = datetime.now().strftime("%d%m%Y%H%M%S")
    invoice_id = f"INV-{timestamp}"
    
    # Save invoice
    cursor.execute("INSERT INTO invoices VALUES (?, ?, ?, ?, ?)", 
                  (invoice_id, username, total_amount, discount, timestamp))
    
    # Save cart items
    for item in items:
        cursor.execute("INSERT INTO cart_items (username, product_name, price, quantity, category) VALUES (?, ?, ?, ?, ?)",
                      (username, item[0], item[1], item[2], item[3]))
    
    conn.commit()
    conn.close()
    return invoice_id

def get_user_id(username):
    conn = sqlite3.connect('schema.db')
    cursor = conn.cursor()
    cursor.execute("SELECT rowid FROM users WHERE username=?", (username,))
    user_id = cursor.fetchone()
    conn.close()
    return user_id[0] if user_id else None

def get_cart_items(username):
    conn = sqlite3.connect('schema.db')
    cursor = conn.cursor()
    cursor.execute("SELECT product_name, price, quantity, category FROM cart_items WHERE username=?", (username,))
    items = cursor.fetchall()
    conn.close()
    return items

# Initialize database on first run
create_tables()