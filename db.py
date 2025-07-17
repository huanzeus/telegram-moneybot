import sqlite3

def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        type TEXT,
        amount INTEGER,
        note TEXT
    )''')
    conn.commit()
    conn.close()

def add_transaction(user_id, date, t_type, amount, note):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("INSERT INTO transactions (user_id, date, type, amount, note) VALUES (?, ?, ?, ?, ?)",
              (user_id, date, t_type, amount, note))
    conn.commit()
    conn.close()

def get_transactions(user_id, date_from, date_to):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT date, type, amount, note FROM transactions WHERE user_id=? AND date BETWEEN ? AND ?",
              (user_id, date_from, date_to))
    data = c.fetchall()
    conn.close()
    return data