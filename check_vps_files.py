#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar arquivos no VPS
"""

import paramiko

VPS_HOST = "72.60.244.240"
VPS_USER = "root"
VPS_PASSWORD = "Amor180725###"
VPS_PORT = 22

def run_ssh_command(ssh, command):
    """Executa comando SSH"""
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode().strip()

print("🔐 Conectando ao VPS...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(VPS_HOST, port=VPS_PORT, username=VPS_USER, password=VPS_PASSWORD, timeout=10)

print("✅ Conectado!")

# Verificar conteúdo do diretório
print("\n📁 Verificando /root/smin_deck_updates/...")
output = run_ssh_command(ssh, "ls -lah /root/smin_deck_updates/ | head -20")
print(output)

# Verificar se vps_update_server.py existe
print("\n🔍 Procurando vps_update_server.py...")
output = run_ssh_command(ssh, "find /root -name 'vps_update_server.py' 2>/dev/null")
print(output if output else "❌ Não encontrado")

# Ver logs
print("\n📋 Últimos logs...")
output = run_ssh_command(ssh, "tail -20 /tmp/update_server.log 2>/dev/null || echo 'Sem logs'")
print(output)

ssh.close()
