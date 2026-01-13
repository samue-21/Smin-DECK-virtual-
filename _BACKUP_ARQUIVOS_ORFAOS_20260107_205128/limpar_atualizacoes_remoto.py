import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.60.244.240', username='root', password='Amor180725###')

# Limpar atualizacoes
cmd = 'sqlite3 ~/.smindeckbot/smindeckbot.db "DELETE FROM atualizacoes;"'
ssh.exec_command(cmd)

# Contar restantes
cmd2 = 'sqlite3 ~/.smindeckbot/smindeckbot.db "SELECT COUNT(*) FROM atualizacoes;"'
stdin, stdout, stderr = ssh.exec_command(cmd2)
count = stdout.read().decode().strip()

print(f'✅ Tabela atualizacoes limpa no remoto (restantes: {count})')

ssh.close()
