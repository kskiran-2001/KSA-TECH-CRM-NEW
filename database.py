import sqlite3

conn = sqlite3.connect("customers.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
number TEXT,
address TEXT,
brand TEXT,
camera INTEGER,
install_date TEXT,
next_service TEXT,
status TEXT
)
""")

conn.commit()

conn.close()

print("Database Created Successfully")
import sqlite3

DATABASE = "customers.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn