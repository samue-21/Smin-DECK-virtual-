import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.60.244.240', username='root', password='Amor180725###')

# Ler bot.py
print("ANALISANDO BOT.PY NA VPS")
print("="*60)

cmd = 'head -100 /opt/smindeck-bot/bot.py'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
print(output)

print("\n" + "="*60)
print("PROCURANDO POR FUNÇÕES DE COMANDO...")
print("="*60)

cmd = 'grep -n "def on_message\|@bot.command\|criar_chave\|validar_chave" /opt/smindeck-bot/bot.py | head -20'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
print(output)

print("\n" + "="*60)
print("VERIFICANDO SE HÁ INFINITO LOOP OU AWAIT...")
print("="*60)

cmd = 'grep -n "while\|await\|time.sleep" /opt/smindeck-bot/bot.py | head -20'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
print(output)

ssh.close()
