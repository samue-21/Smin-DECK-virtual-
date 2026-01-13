#!/usr/bin/env python3
"""
Verificar bot no VPS - Script Python com subprocess direto
Usa o cliente SSH do sistema operacional
"""

import subprocess
import platform
import sys

VPS_HOST = "72.60.244.240"
VPS_USER = "root"

def run_command(cmd):
    """Executa comando e retorna output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=20
        )
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "❌ TIMEOUT - Conexão demorou muito"
    except Exception as e:
        return f"❌ Erro: {str(e)}"

def check_bot_status():
    """Verifica status do bot no VPS"""
    
    print("\n" + "="*70)
    print("🔗 VERIFICANDO BOT NO VPS")
    print("="*70)
    
    # 1. Testar conectividade
    print("\n⏳ Testando conectividade com VPS...")
    ping_cmd = f"ping -c 1 {VPS_HOST}" if platform.system() != "Windows" else f"ping -n 1 {VPS_HOST}"
    result = run_command(ping_cmd)
    if "Reply from" in result or "bytes from" in result or "time=" in result:
        print("✅ VPS está online")
    else:
        print("⚠️  Possível problema de conectividade")
    
    # 2. Status do bot
    print("\n📊 STATUS DO BOT")
    print("-" * 70)
    cmd = f"ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no {VPS_USER}@{VPS_HOST} 'systemctl status smindeck-bot --no-pager' 2>&1"
    output = run_command(cmd)
    lines = output.split('\n')
    # Mostrar apenas linhas relevantes
    for line in lines[:15]:
        if line.strip():
            print(line)
    
    # 3. Logs recentes
    print("\n📋 ÚLTIMAS 25 LINHAS DOS LOGS")
    print("-" * 70)
    cmd = f"ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no {VPS_USER}@{VPS_HOST} 'tail -25 /opt/smindeck-bot/debug.log' 2>&1"
    output = run_command(cmd)
    print(output)
    
    # 4. Procurar erros
    print("\n⚠️  VERIFICANDO ERROS")
    print("-" * 70)
    cmd = f"ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no {VPS_USER}@{VPS_HOST} \"tail -50 /opt/smindeck-bot/debug.log | grep -i 'error\\|exception\\|failed' || echo 'Nenhum erro encontrado'\" 2>&1"
    output = run_command(cmd)
    print(output)
    
    # 5. Processos
    print("\n🔍 PROCESSOS PYTHON")
    print("-" * 70)
    cmd = f"ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no {VPS_USER}@{VPS_HOST} 'ps aux | grep -E \"bot\\.py|api_server\" | grep -v grep' 2>&1"
    output = run_command(cmd)
    if output.strip():
        print(output)
    else:
        print("❌ Nenhum processo encontrado!")
    
    print("\n" + "="*70)
    print("✅ Verificação concluída!")
    print("="*70 + "\n")

if __name__ == "__main__":
    check_bot_status()
