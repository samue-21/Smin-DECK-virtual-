import sqlite3
import os

db_path = os.path.expanduser('~/.smindeckbot/smindeckbot.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Ver schema da tabela atualizacoes
cursor.execute("PRAGMA table_info(atualizacoes)")
columns = cursor.fetchall()

print("Colunas da tabela 'atualizacoes':")
for col in columns:
    print(f"  - {col[1]} ({col[2]})")

# Contar linhas
cursor.execute("SELECT COUNT(*) FROM atualizacoes")
count = cursor.fetchone()[0]
print(f"\nTotal de linhas: {count}")

if count > 0:
    # Ver primeiras linhas
    cursor.execute("SELECT * FROM atualizacoes LIMIT 3")
    rows = cursor.fetchall()
    print("\nPrimeiras linhas:")
    for row in rows:
        print(f"  {row}")

conn.close()
