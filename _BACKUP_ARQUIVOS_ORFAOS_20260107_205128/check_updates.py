#!/usr/bin/env python3
import paramiko
import sqlite3
import os

# Verificar no VPS
print("=== VERIFICANDO NO VPS ===")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='72.60.244.240', username='root', password='Amor180725###', port=22)

# Atualizações VPS
stdin, stdout, stderr = ssh.exec_command('sqlite3 ~/.smindeckbot/smindeckbot.db "SELECT id, chave, tipo, botao FROM atualizacoes;"')
print('Atualizações (VPS):')
result = stdout.read().decode()
print(result if result.strip() else '(vazio)')

# Chaves VPS
stdin, stdout, stderr = ssh.exec_command('sqlite3 ~/.smindeckbot/smindeckbot.db "SELECT chave, user_id FROM chaves_ativas;"')
print('\nChaves Ativas (VPS):')
print(stdout.read().decode())

ssh.close()

# Verificar localmente também
print("\n=== VERIFICANDO LOCALMENTE ===")
local_db = os.path.expanduser('~/.smindeckbot/smindeckbot.db')
if os.path.exists(local_db):
    conn = sqlite3.connect(local_db)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM atualizacoes')
    print('Atualizações (Local):')
    for row in cursor.fetchall():
        print(row)
    
    conn.close()
else:
    print('(banco local não existe)')
