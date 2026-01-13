#!/usr/bin/env python3
"""
Inicia API manualmente no VPS
"""

import paramiko

VPS_HOST = "72.60.244.240"
VPS_USER = "root"
VPS_PASSWORD = "Amor180725###"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(VPS_HOST, username=VPS_USER, password=VPS_PASSWORD)

# Inicia API em background
print("Iniciando API no VPS...")
stdin, stdout, stderr = ssh.exec_command("cd /opt/smindeck-bot && nohup python3 api_server.py > /opt/smindeck-bot/api.log 2>&1 &")
stdout.read()

# Aguarda um pouco
import time
time.sleep(2)

# Verifica se está rodando
print("Verificando API...")
stdin, stdout, stderr = ssh.exec_command("ps aux | grep api_server")
output = stdout.read().decode()
if "api_server.py" in output and "grep" not in output:
    print("✅ API iniciada com sucesso!")
    print(output)
else:
    print("⚠️  Verificando logs...")
    stdin, stdout, stderr = ssh.exec_command("tail -20 /opt/smindeck-bot/api.log")
    print(stdout.read().decode())

ssh.close()
