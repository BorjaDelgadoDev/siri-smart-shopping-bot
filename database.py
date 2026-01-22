import sqlite3
import os

DB_PATH = "compra.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabla items: id, name, category, quantity, created_at
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT DEFAULT 'Otros 📦',
            quantity TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla bot_state: key (PK), value
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bot_state (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def add_item(name, quantity, category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (name, quantity, category) VALUES (?, ?, ?)",
        (name, quantity, category)
    )
    conn.commit()
    conn.close()

def get_all_items():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, quantity, category FROM items ORDER BY category ASC")
    items = cursor.fetchall()
    conn.close()
    return items

def delete_item(item_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def set_state(key, value):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO bot_state (key, value) VALUES (?, ?)",
        (key, str(value))
    )
    conn.commit()
    conn.close()

def get_state(key):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM bot_state WHERE key = ?", (key,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
