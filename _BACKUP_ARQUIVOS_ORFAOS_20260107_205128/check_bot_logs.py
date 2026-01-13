#!/usr/bin/env python3
"""Verificar bot no VPS usando SSH com senha - Versão simplificada"""

import subprocess
import sys
import os

VPS_HOST = "72.60.244.240"
VPS_USER = "root"
VPS_PASSWORD = "Amor180725###"

def run_ssh_command(command):
    """Executa comando no VPS usando SSH com sshpass"""
    try:
        # Tenta usar sshpass se disponível (Linux/Mac)
        cmd = f'sshpass -p "{VPS_PASSWORD}" ssh -o StrictHostKeyChecking=no -l {VPS_USER} {VPS_HOST} "{command}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Erro: {e}"

print("🔗 Conectando ao VPS...")
print("="*70)

# 1. Status do bot
print("\n📊 STATUS DO BOT\n")
output = run_ssh_command("systemctl status smindeck-bot 2>&1")
print(output[:2000])  # Limitar output

# 2. Debug logs
print("\n📋 ÚLTIMAS 30 LINHAS DOS LOGS\n")
output = run_ssh_command("tail -30 /opt/smindeck-bot/debug.log 2>&1")
print(output)

# 3. Procurar erros
print("\n⚠️  PROCURANDO ERROS\n")
output = run_ssh_command("grep -i 'error\\|exception\\|traceback' /opt/smindeck-bot/debug.log | tail -15 2>&1")
if output.strip():
    print(output)
else:
    print("✅ Nenhum erro encontrado\n")

# 4. Ver processos
print("\n🔍 PROCESSOS RODANDO\n")
output = run_ssh_command("ps aux | grep -E 'bot.py|api_server' | grep -v grep 2>&1")
print(output)

print("\n✅ Verificação concluída!")
