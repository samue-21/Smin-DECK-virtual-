#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar logs do VPS
"""
import paramiko
import sys
import io

# Forçar UTF-8
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

VPS_HOST = "72.60.244.240"
VPS_USER = "root"
VPS_PASSWORD = "Amor180725###"

def check_logs():
    """Conecta ao VPS e mostra logs do bot"""
    print("🔐 Conectando ao VPS...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(VPS_HOST, username=VPS_USER, password=VPS_PASSWORD, timeout=10)
        print("✅ Conectado ao VPS!\n")
        
        # Ver logs do bot
        print("=" * 60)
        print("📋 ÚLTIMOS LOGS DO BOT")
        print("=" * 60)
        
        stdin, stdout, stderr = ssh.exec_command("tail -150 /opt/smindeck-bot/debug.log 2>/dev/null || echo 'Log não encontrado'")
        output = stdout.read().decode('utf-8', errors='ignore')
        print(output)
        
        # Status do bot
        print("\n" + "=" * 60)
        print("⚡ STATUS DO BOT")
        print("=" * 60)
        stdin, stdout, stderr = ssh.exec_command("systemctl status smindeck-bot")
        output = stdout.read().decode('utf-8', errors='ignore')
        print(output[:500])
        
        # Ver arquivos no uploads
        print("\n" + "=" * 60)
        print("📁 ARQUIVOS EM /opt/smindeck-bot/uploads/")
        print("=" * 60)
        stdin, stdout, stderr = ssh.exec_command("ls -lah /opt/smindeck-bot/uploads/ | tail -20")
        output = stdout.read().decode('utf-8', errors='ignore')
        print(output)
        
        ssh.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_logs()
