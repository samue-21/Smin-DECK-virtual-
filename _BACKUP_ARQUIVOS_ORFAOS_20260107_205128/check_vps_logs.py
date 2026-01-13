#!/usr/bin/env python3
"""
Script para conectar ao VPS e verificar logs do bot usando paramiko
"""

import sys
import os

# Tentar importar paramiko, se não estiver instalado, instala
try:
    import paramiko
except ImportError:
    print("📦 Instalando paramiko...")
    os.system(f"{sys.executable} -m pip install paramiko -q")
    import paramiko

import warnings
warnings.filterwarnings('ignore')

VPS_IP = "72.60.244.240"
VPS_USER = "root"
VPS_PASSWORD = "Amor180725###"

print("🔌 Conectando ao VPS...")
print(f"   IP: {VPS_IP}")
print(f"   Usuário: {VPS_USER}")
print()

try:
    # Criar cliente SSH
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Conectar com timeout
    ssh_client.connect(
        VPS_IP,
        username=VPS_USER,
        password=VPS_PASSWORD,
        timeout=10,
        look_for_keys=False,
        allow_agent=False
    )
    
    print("✅ Conectado com sucesso!\n")
    
    # Comando para verificar status do bot
    commands = [
        ("echo '=== STATUS DO BOT ===' && systemctl status smindeck-bot --no-pager", "Status do Bot"),
        ("echo '\n=== ÚLTIMAS 60 LINHAS DO LOG ===' && tail -60 /opt/smindeck-bot/debug.log", "Logs do Bot"),
        ("echo '\n=== PROCESSOS PYTHON ===' && ps aux | grep python3 | grep -v grep", "Processos Python"),
    ]
    
    for cmd, desc in commands:
        print(f"\n{'='*60}")
        print(f"📋 {desc}")
        print('='*60)
        
        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        
        output = stdout.read().decode('utf-8', errors='ignore')
        error = stderr.read().decode('utf-8', errors='ignore')
        
        if output:
            print(output)
        if error:
            print(f"⚠️  {error}")
    
    ssh_client.close()
    print("\n✅ Desconectado do VPS")
    
except paramiko.AuthenticationException:
    print("❌ Erro de autenticação - Verifique a senha")
except paramiko.SSHException as e:
    print(f"❌ Erro SSH: {e}")
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
