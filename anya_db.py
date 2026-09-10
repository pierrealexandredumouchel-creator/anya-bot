import sqlite3
from datetime import datetime

DB = "anya.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS seen (user TEXT PRIMARY KEY, last_seen TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS quotes (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, quote TEXT)")
    conn.commit()
    conn.close()

def log_seen(user):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("REPLACE INTO seen VALUES (?, ?)", (user, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_seen(user):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT last_seen FROM seen WHERE user=?", (user,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def add_quote(user, quote):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO quotes (user, quote) VALUES (?, ?)", (user, quote))
    conn.commit()
    conn.close()

def random_quote():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT user, quote FROM quotes ORDER BY RANDOM() LIMIT 1")
    row = c.fetchone()
    conn.close()
    return row if row else None
