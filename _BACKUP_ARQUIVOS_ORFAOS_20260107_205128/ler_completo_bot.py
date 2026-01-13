import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.60.244.240', username='root', password='Amor180725###')

# Ler a função on_message COMPLETA
cmd = 'sed -n "443,550p" /opt/smindeck-bot/bot.py'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
print("ON_MESSAGE COMPLETO:")
print(output)

print("\n" + "="*60)
print("PROCURANDO POR TRATAMENTO DE ERROS...")
print("="*60)

cmd = 'grep -n "except\|try:" /opt/smindeck-bot/bot.py | head -15'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
print(output)

ssh.close()
