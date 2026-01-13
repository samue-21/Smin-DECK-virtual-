import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.60.244.240', username='root', password='Amor180725###')

# Executar Python na VPS para limpar
cmd = '''python3 -c "
import sqlite3
import os

db = os.path.expanduser('~/.smindeckbot/smindeckbot.db')
conn = sqlite3.connect(db)
cursor = conn.cursor()

cursor.execute('DELETE FROM atualizacoes')
conn.commit()

cursor.execute('SELECT COUNT(*) FROM atualizacoes')
count = cursor.fetchone()[0]

print(f'✅ Limpeza completa! Atualizações restantes: {count}')
conn.close()
"'''

stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())
err = stderr.read().decode()
if err:
    print(f"Erro: {err}")

ssh.close()
