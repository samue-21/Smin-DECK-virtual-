import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.60.244.240', username='root', password='Amor180725###')

print("ENVIANDO BOT.PY CORRIGIDO PARA VPS")
print("="*60)

# Ler o arquivo local
with open('C:\\Users\\SAMUEL\\Desktop\\Smin-DECK virtual\\bot.py', 'r') as f:
    content = f.read()

# Enviar via SFTP
sftp = ssh.open_sftp()
sftp.putfo(open('C:\\Users\\SAMUEL\\Desktop\\Smin-DECK virtual\\bot.py', 'rb'), '/opt/smindeck-bot/bot.py')
sftp.close()

print("1️⃣ Arquivo enviado")

# Reiniciar bot
cmd = 'pkill -9 -f "bot.py" ; sleep 2 ; cd /opt/smindeck-bot && nohup python3 bot.py > bot.log 2>&1 &'
stdin, stdout, stderr = ssh.exec_command(cmd)
import time
time.sleep(3)
print("2️⃣ Bot reiniciado")

# Verificar
cmd = 'ps aux | grep bot.py | grep -v grep'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
if output.strip():
    print("   ✅ Bot rodando")
else:
    print("   ❌ Erro ao iniciar bot")
    cmd = 'cat /opt/smindeck-bot/bot.log | tail -20'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode())

ssh.close()

print("\n" + "="*60)
print("✅ BOT ATUALIZADO!")
