import sqlite3
import os

db_path = os.path.expanduser('~/.smindeckbot/data.db')

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    print("Tabelas:", tables)
    conn.close()
except Exception as e:
    print(f"Erro: {e}")
