import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.60.244.240', username='root', password='Amor180725###', timeout=10)
sftp = ssh.open_sftp()

# Criar script no VPS
script = """import sqlite3, os
db = os.path.expanduser('~/.smindeckbot/smindeckbot.db')
conn = sqlite3.connect(db)
c = conn.cursor()
print('TABELAS:')
c.execute('SELECT name FROM sqlite_master WHERE type="table"')
for r in c.fetchall(): print(r[0])
print('\\nATUALIZACOES:')
c.execute('SELECT * FROM atualizacoes')
for r in c.fetchall(): print(r)
print('\\nCHAVES_ATIVAS:')
c.execute('SELECT * FROM chaves_ativas')
for r in c.fetchall(): print(r)
conn.close()
"""

with sftp.file('/tmp/check_db.py', 'w') as f:
    f.write(script)
sftp.close()

_, o, e = ssh.exec_command('python3 /tmp/check_db.py')
print(o.read().decode())
err = e.read().decode()
if err.strip():
    print('Err:', err)
ssh.close()
