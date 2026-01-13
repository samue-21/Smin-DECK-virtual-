import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.60.244.240', username='root', password='Amor180725###')

# Ler a função gerar_chave
cmd = 'sed -n "225,235p" /opt/smindeck-bot/bot.py'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
print("FUNÇÃO GERAR_CHAVE:")
print(output)

print("\n" + "="*60)

# Ler on_message
cmd = 'sed -n "443,480p" /opt/smindeck-bot/bot.py'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
print("FUNÇÃO ON_MESSAGE:")
print(output)

ssh.close()
