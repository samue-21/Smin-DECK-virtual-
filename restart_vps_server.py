#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar e reiniciar servidor de updates no VPS
"""

import paramiko
import time

VPS_HOST = "72.60.244.240"
VPS_USER = "root"
VPS_PASSWORD = "Amor180725###"
VPS_PORT = 22

def run_ssh_command(ssh, command):
    """Executa comando SSH"""
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode().strip(), stderr.read().decode().strip()

print("🔐 Conectando ao VPS...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(VPS_HOST, port=VPS_PORT, username=VPS_USER, password=VPS_PASSWORD, timeout=10)

print("✅ Conectado!")

# 1. Verificar status do servidor
print("\n1️⃣ Checando status...")
output, error = run_ssh_command(ssh, "ps aux | grep vps_update_server")
print(output)

# 2. Parar servidor anterior
print("\n2️⃣ Parando servidor anterior...")
output, error = run_ssh_command(ssh, "pkill -f vps_update_server")
print("✅ Parado")

time.sleep(2)

# 3. Reiniciar servidor
print("\n3️⃣ Iniciando novo servidor...")
output, error = run_ssh_command(ssh, "cd /root/smin_deck_updates && nohup python vps_update_server.py > /tmp/update_server.log 2>&1 &")
print("✅ Iniciado")

time.sleep(3)

# 4. Verificar se está rodando
print("\n4️⃣ Verificando se está respondendo...")
output, error = run_ssh_command(ssh, "curl -s http://localhost:8001/health")
print(f"Resposta: {output}")

# 5. Testar endpoint
print("\n5️⃣ Testando /api/updates/check...")
output, error = run_ssh_command(ssh, "curl -s http://localhost:8001/api/updates/check")
print(f"Resposta: {output[:200]}")

ssh.close()
print("\n✅ Concluído!")
