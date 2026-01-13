#!/usr/bin/env python3
import sqlite3
import paramiko
from pathlib import Path

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='72.60.244.240', username='root', password='Amor180725###', port=22)

# Copiar banco para cá
sftp = ssh.open_sftp()
sftp.get('/root/.smindeckbot/smindeckbot.db', '/tmp/test.db')
sftp.close()
ssh.close()

# Verificar localmente
conn = sqlite3.connect('/tmp/test.db')
cursor = conn.cursor()

# Listar tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tabelas encontradas:')
for table in tables:
    print(f'  - {table[0]}')
    
    # Listar dados dessa tabela
    cursor.execute(f'SELECT * FROM {table[0]}')
    rows = cursor.fetchall()
    print(f'    Registros: {len(rows)}')
    for row in rows[:3]:  # Primeiros 3
        print(f'      {row}')

conn.close()
