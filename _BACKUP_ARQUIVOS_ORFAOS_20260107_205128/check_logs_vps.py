#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar logs do bot no VPS usando Paramiko
"""

import paramiko
import sys
import os

# Forçar UTF-8 no Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Credenciais
VPS_HOST = "72.60.244.240"
VPS_USER = "root"
VPS_PASSWORD = "Amor180725###"

def connect_ssh():
    """Conecta ao VPS via SSH"""
    print("🔐 Conectando ao VPS...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(VPS_HOST, username=VPS_USER, password=VPS_PASSWORD, timeout=10)
        print("✅ Autenticado!\n")
        return ssh
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        sys.exit(1)

def run_command(ssh, command, title=""):
    """Executa comando e mostra resultado"""
    if title:
        print("\n" + "="*70)
        print(title)
        print("="*70)
    
    try:
        stdin, stdout, stderr = ssh.exec_command(command, timeout=10)
        output = stdout.read().decode('utf-8', errors='replace')
        error = stderr.read().decode('utf-8', errors='replace')
        
        if output.strip():
            print(output)
        if error.strip():
            print("⚠️  " + error)
            
        return output + error
    except Exception as e:
        print(f"❌ Erro ao executar comando: {e}")
        return ""

def check_logs():
    """Verifica logs do bot"""
    
    print("\n" + "="*70)
    print("🔍 VERIFICADOR DE LOGS DO BOT")
    print("="*70)
    
    ssh = connect_ssh()
    
    try:
        # 1. Status do bot
        run_command(ssh, 
            "systemctl status smindeck-bot --no-pager | head -20",
            "📊 STATUS DO BOT"
        )
        
        # 2. Logs recentes
        run_command(ssh,
            "tail -40 /opt/smindeck-bot/debug.log",
            "📋 ÚLTIMAS 40 LINHAS DOS LOGS"
        )
        
        # 3. Verificar se bot está respondendo
        print("\n" + "="*70)
        print("🤖 TESTE DE RESPONSIVIDADE")
        print("="*70)
        
        stdin, stdout, stderr = ssh.exec_command(
            "ps aux | grep 'bot.py' | grep -v grep"
        )
        ps_output = stdout.read().decode('utf-8', errors='replace')
        
        if 'python3' in ps_output and 'bot.py' in ps_output:
            print("✅ Bot ESTÁ RODANDO")
            # Extrair PID
            parts = ps_output.split()
            if len(parts) > 1:
                pid = parts[1]
                print(f"   PID: {pid}")
                print(f"   Memória: {parts[5] if len(parts) > 5 else 'N/A'}")
        else:
            print("❌ Bot NÃO ESTÁ RODANDO!")
        
        # 4. Verificar erros
        print("\n" + "="*70)
        print("⚠️  PROCURANDO ERROS E EXCEÇÕES")
        print("="*70 + "\n")
        
        stdin, stdout, stderr = ssh.exec_command(
            "grep -i 'error\\|exception\\|traceback\\|failed' /opt/smindeck-bot/debug.log | tail -20"
        )
        errors = stdout.read().decode('utf-8', errors='replace')
        
        if errors.strip():
            print("Erros encontrados:\n")
            print(errors)
        else:
            print("✅ Nenhum erro encontrado nos logs\n")
        
        # 5. Verificar API
        print("\n" + "="*70)
        print("🔌 STATUS DA API")
        print("="*70)
        
        run_command(ssh,
            "systemctl status smindeck-api --no-pager | head -15",
            ""
        )
        
        # 6. Ver conexões ativas
        print("\n" + "="*70)
        print("📡 VERIFICANDO CONEXÕES COM DISCORD")
        print("="*70 + "\n")
        
        stdin, stdout, stderr = ssh.exec_command(
            "tail -5 /opt/smindeck-bot/debug.log"
        )
        latest = stdout.read().decode('utf-8', errors='replace')
        
        if "ready" in latest.lower() or "logged in" in latest.lower():
            print("✅ Bot conectado ao Discord")
        else:
            print("⚠️  Verificar status de conexão")
        
        print("\n" + latest)
        
    finally:
        ssh.close()
        print("\n✅ Verificação concluída!")

if __name__ == "__main__":
    try:
        check_logs()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
