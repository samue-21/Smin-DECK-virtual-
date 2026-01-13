#!/usr/bin/env python3
"""
Script para verificar .env no VPS
"""
import sys
import os

# Adicionar deploy_vps_auto ao path
sys.path.insert(0, os.path.dirname(__file__))

try:
    import paramiko
except ImportError:
    print("Instalando paramiko...")
    os.system(f"{sys.executable} -m pip install paramiko -q")
    import paramiko

import warnings
warnings.filterwarnings('ignore')

VPS_IP = "72.60.244.240"
VPS_USER = "root"
VPS_PASSWORD = "Amor180725###"

print("[*] Conectando ao VPS...")

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(VPS_IP, username=VPS_USER, password=VPS_PASSWORD, timeout=15, look_for_keys=False, allow_agent=False)
    
    print("[+] Conectado!")
    
    # Verificar .env
    print("\n[*] Lendo arquivo .env...")
    stdin, stdout, stderr = ssh.exec_command("cat /opt/smindeck-bot/.env 2>/dev/null || echo 'Arquivo nao encontrado'")
    env_content = stdout.read().decode('utf-8', errors='ignore')
    print(env_content)
    
    # Verificar logs
    print("\n[*] Ultimas 20 linhas do debug.log...")
    stdin, stdout, stderr = ssh.exec_command("tail -20 /opt/smindeck-bot/debug.log 2>/dev/null")
    logs = stdout.read().decode('utf-8', errors='ignore')
    print(logs)
    
    ssh.close()
    print("\n[+] Desconectado")

except Exception as e:
    print(f"[-] Erro: {e}")
    import traceback
    traceback.print_exc()
