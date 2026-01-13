import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.60.244.240', username='root', password='Amor180725###')

# Ver linhas críticas do bot.py - onde chama criar_chave
cmd = 'sed -n "456,470p" /opt/smindeck-bot/bot.py'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
print("🤖 BOT.PY - LINHAS 456-470 (CRIAR CHAVE):")
print(output)

print("\n" + "="*60)

# Ver função usuario_autenticado
cmd = 'grep -n "def usuario_autenticado" /opt/smindeck-bot/bot.py'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
print("🔍 PROCURANDO usuario_autenticado:")
print(output)

if output.strip():
    # Pegar linha
    line = output.split(':')[0]
    cmd = f'sed -n "{line},{int(line)+10}p" /opt/smindeck-bot/bot.py'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode()
    print("\nCÓDIGO:")
    print(output)

ssh.close()
