#!/usr/bin/env python3
import sqlite3, os

db_path = os.path.expanduser('~/.smindeckbot/smindeckbot.db')
if os.path.exists(db_path):
    print(f'✓ Banco existe: {db_path}')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f'✓ Tabelas: {tables}')
    
    # Contar atualizações
    try:
        cursor.execute('SELECT COUNT(*) FROM atualizacoes')
        count = cursor.fetchone()[0]
        print(f'✓ Total de atualizações: {count}')
    except Exception as e:
        print(f'✗ Erro ao contar: {e}')
    
    conn.close()
else:
    print(f'✗ Banco NÃO existe: {db_path}')
    print(f'✗ Crie com: python database.py')
