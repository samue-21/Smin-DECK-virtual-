#!/usr/bin/env python3
"""
🤖 Script de Automação VPS - Conecta, copia arquivos, reinicia bot
"""

import paramiko
import sys
import os
from pathlib import Path
import time

# Importa config
from vps_config import VPS_CONFIG

def conectar_vps():
    """Conecta ao VPS via SSH"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"🔗 Conectando a {VPS_CONFIG['host']}...")
        ssh.connect(
            hostname=VPS_CONFIG['host'],
            port=VPS_CONFIG['port'],
            username=VPS_CONFIG['user'],
            password=VPS_CONFIG['password'],
            timeout=10,
            banner_timeout=10
        )
        print("✅ Conectado ao VPS!")
        return ssh
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        sys.exit(1)

def enviar_arquivo(ssh, local_path, remote_path):
    """Envia arquivo via SFTP"""
    try:
        print(f"📤 Enviando {Path(local_path).name}...")
        sftp = ssh.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()
        print(f"✅ {Path(local_path).name} enviado!")
    except Exception as e:
        print(f"❌ Erro ao enviar: {e}")
        sys.exit(1)

def executar_comando(ssh, cmd):
    """Executa comando no VPS"""
    try:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read().decode('utf-8', errors='ignore')
        error = stderr.read().decode('utf-8', errors='ignore')
        
        if output:
            print(output.strip())
        if error and "not found" not in error.lower():
            print(f"⚠️  {error.strip()}")
        
        return output, error
    except Exception as e:
        print(f"❌ Erro ao executar comando: {e}")
        return "", str(e)

def restart_bot(ssh):
    """Reinicia o bot"""
    print("\n🔄 Reiniciando bot...")
    cmd = """
    cd /opt/smindeck-bot
    pkill -f 'python.*bot.py' 2>/dev/null
    sleep 2
    nohup python3 bot.py > bot_output.log 2>&1 &
    sleep 1
    echo "✅ Bot iniciado"
    """
    executar_comando(ssh, cmd)

def ver_logs(ssh, linhas=30):
    """Mostra últimas linhas do log do bot"""
    print(f"\n📋 Últimas {linhas} linhas do log:")
    cmd = f"tail -n {linhas} /opt/smindeck-bot/bot_output.log 2>/dev/null || echo 'Log ainda não criado'"
    executar_comando(ssh, cmd)

def main():
    """Menu principal"""
    print("\n" + "="*50)
    print("🚀 Automação VPS - SminDeck Bot")
    print("="*50 + "\n")
    
    if len(sys.argv) > 1:
        acao = sys.argv[1].lower()
    else:
        print("Opções:")
        print("  python auto_vps.py enviar    → Enviar bot.py e reiniciar")
        print("  python auto_vps.py logs      → Ver logs do bot")
        print("  python auto_vps.py comando   → Executar comando personalizado")
        print("\nExemplo: python auto_vps.py enviar")
        return
    
    ssh = conectar_vps()
    
    try:
        if acao == "enviar":
            local_bot = r"c:\Users\SAMUEL\Desktop\Smin-DECK virtual\bot.py"
            remote_bot = "/opt/smindeck-bot/bot.py"
            
            if not os.path.exists(local_bot):
                print(f"❌ Arquivo não encontrado: {local_bot}")
                sys.exit(1)
            
            enviar_arquivo(ssh, local_bot, remote_bot)
            restart_bot(ssh)
            time.sleep(2)
            ver_logs(ssh, linhas=20)
            
        elif acao == "logs":
            ver_logs(ssh, linhas=50)
        
        elif acao == "status":
            print("\n🔍 Status dos processos Python:")
            executar_comando(ssh, "ps aux | grep python | grep -v grep")
            
        elif acao == "comando":
            if len(sys.argv) < 3:
                print("❌ Use: python auto_vps.py comando 'seu comando aqui'")
                return
            cmd = " ".join(sys.argv[2:])
            executar_comando(ssh, cmd)
            
        else:
            print(f"❌ Ação desconhecida: {acao}")
            
    finally:
        ssh.close()
        print("\n✅ Desconectado do VPS")

if __name__ == "__main__":
    main()
