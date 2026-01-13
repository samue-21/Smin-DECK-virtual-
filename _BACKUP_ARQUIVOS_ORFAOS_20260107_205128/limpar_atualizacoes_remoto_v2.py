import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.60.244.240', username='root', password='Amor180725###')

# Primeiro, listar
cmd = 'sqlite3 ~/.smindeckbot/smindeckbot.db "SELECT COUNT(*) FROM atualizacoes;"'
stdin, stdout, stderr = ssh.exec_command(cmd)
before = stdout.read().decode().strip()
print(f"Antes: {before} atualizações")

# Limpar
cmd2 = 'sqlite3 ~/.smindeckbot/smindeckbot.db "DELETE FROM atualizacoes;"'
stdin, stdout, stderr = ssh.exec_command(cmd2)
err = stderr.read().decode()
if err:
    print(f"Erro: {err}")

# Verificar depois
cmd3 = 'sqlite3 ~/.smindeckbot/smindeckbot.db "SELECT COUNT(*) FROM atualizacoes;"'
stdin, stdout, stderr = ssh.exec_command(cmd3)
after = stdout.read().decode().strip()
print(f"Depois: {after} atualizações")

# Mostrar também o conteúdo
cmd4 = 'sqlite3 ~/.smindeckbot/smindeckbot.db "SELECT * FROM atualizacoes;"'
stdin, stdout, stderr = ssh.exec_command(cmd4)
content = stdout.read().decode()
if content.strip():
    print(f"Conteúdo:\n{content}")
else:
    print("Tabela vazia!")

ssh.close()
