#!/usr/bin/env python3
import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='72.60.244.240', username='root', password='Amor180725###', port=22)

print("🛑 Matando bot antigo...")
ssh.exec_command("pkill -9 -f bot.py")
time.sleep(2)

print("🗑️ Limpando banco...")
ssh.exec_command("rm -f ~/.smindeckbot/smindeckbot.db")

print("🚀 Iniciando bot novo...")
ssh.exec_command("cd /opt/smindeck-bot && nohup python3 bot.py > bot.log 2>&1 &")
time.sleep(3)

# Verificar
stdin, stdout, stderr = ssh.exec_command("ps aux | grep python3 | grep bot.py | grep -v grep")
if stdout.read().decode().strip():
    print("✅ Bot iniciado com sucesso!")
else:
    print("❌ Erro ao iniciar. Verificando:")
    stdin, stdout, stderr = ssh.exec_command("cat /opt/smindeck-bot/bot.log")
    print(stdout.read().decode())

ssh.close()
