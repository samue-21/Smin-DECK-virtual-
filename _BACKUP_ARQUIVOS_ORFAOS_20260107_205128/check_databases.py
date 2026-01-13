import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.60.244.240', username='root', password='Amor180725###')

# Ver qual banco database.py usa
cmd = 'grep "smindeckbot\|smindeck_bot" /opt/smindeck-bot/database.py | head -10'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
print('DATABASE.PY - Qual banco usa:')
print(output if output.strip() else '  (não encontrado)')

# Ver tamanho dos bancos
cmd = 'ls -lh ~/.smindeckbot/smindeck*.db'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
print('\n📁 Tamanho dos bancos:')
print(output)

# Ver quantas chaves em cada banco
cmd = '''python3 << 'EOF'
import sqlite3
import os

db1 = os.path.expanduser("~/.smindeckbot/smindeck_bot.db")
db2 = os.path.expanduser("~/.smindeckbot/smindeckbot.db")

for db_path in [db1, db2]:
    if os.path.exists(db_path):
        name = os.path.basename(db_path)
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM chaves_ativas")
            count = cursor.fetchone()[0]
            print(f"{name}: {count} chaves ativas")
            conn.close()
        except Exception as e:
            print(f"{name}: erro - {e}")
EOF'''

stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
print('\n🔑 Chaves em cada banco:')
print(output)

ssh.close()
