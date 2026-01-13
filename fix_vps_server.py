#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Iniciar servidor de updates corretamente no VPS
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
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    return output, error

print("🔐 Conectando ao VPS...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(VPS_HOST, port=VPS_PORT, username=VPS_USER, password=VPS_PASSWORD, timeout=10)

print("✅ Conectado!")

# 1. Parar servidor anterior
print("\n1️⃣ Parando servidor anterior...")
output, error = run_ssh_command(ssh, "pkill -f vps_update_server || true")
time.sleep(2)

# 2. Iniciar com python3
print("\n2️⃣ Iniciando novo servidor (com python3)...")
output, error = run_ssh_command(ssh, "cd /root && nohup python3 vps_update_server.py > /tmp/update_server.log 2>&1 &")
print("✅ Iniciado")

time.sleep(3)

# 3. Verificar se está rodando
print("\n3️⃣ Verificando processo...")
output, error = run_ssh_command(ssh, "ps aux | grep vps_update_server | grep -v grep")
if output:
    print("✅ Servidor rodando:")
    print(output)
else:
    print("❌ Processo não encontrado")

# 4. Testar porta
print("\n4️⃣ Testando se porta 8001 está aberta...")
output, error = run_ssh_command(ssh, "netstat -tuln | grep 8001 || lsof -i :8001 || echo 'Porta não escutando'")
print(output if output else error)

# 5. Testar endpoint localmente
print("\n5️⃣ Testando endpoint localmente...")
output, error = run_ssh_command(ssh, "curl -s http://localhost:8001/health || echo 'Falhou'")
print(f"Resposta: {output[:100]}")

# 6. Ver logs
print("\n6️⃣ Últimos logs...")
output, error = run_ssh_command(ssh, "tail -30 /tmp/update_server.log")
print(output)

ssh.close()
print("\n✅ Concluído!")
