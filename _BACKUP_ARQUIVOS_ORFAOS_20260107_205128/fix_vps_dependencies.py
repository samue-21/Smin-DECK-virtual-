#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corrigir dependências do Playwright no VPS
Instalar bibliotecas de sistema necessárias
"""

import paramiko
import sys
import os
import time

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

def run_command(ssh, command, title="", show_output=True):
    """Executa comando e mostra resultado"""
    if title:
        print(f"\n{title}")
        print("-" * 70)
    
    try:
        stdin, stdout, stderr = ssh.exec_command(command, timeout=120)
        output = stdout.read().decode('utf-8', errors='replace')
        error = stderr.read().decode('utf-8', errors='replace')
        
        if show_output:
            if output.strip():
                print(output[-500:])  # Mostrar últimas 500 chars
            if error.strip():
                print("⚠️  " + error[-300:])
        
        return output + error
    except Exception as e:
        print(f"❌ Erro: {e}")
        return ""

def fix_dependencies():
    """Corrige dependências no VPS"""
    
    print("\n" + "="*70)
    print("🔧 CORRIGINDO DEPENDÊNCIAS DO PLAYWRIGHT")
    print("="*70)
    
    ssh = connect_ssh()
    
    try:
        # 1. Atualizar package manager
        print("\n📦 Atualizando gerenciador de pacotes...")
        run_command(ssh, "apt-get update -qq", show_output=False)
        print("✅ Atualizado")
        
        # 2. Instalar dependências do Playwright/Chromium
        print("\n📦 Instalando dependências de biblioteca...")
        
        deps_to_install = [
            "libatk-1.0-0",           # Faltava esse!
            "libatk-bridge2.0-0",
            "libatspi2.0-0",
            "libcairo2",
            "libcups2",
            "libdbus-1-3",
            "libexpat1",
            "libgbm1",
            "libgdk-pixbuf2.0-0",
            "libglib2.0-0",
            "libglib2.0-bin",
            "libgtk-3-0",
            "libgtk-3-common",
            "libice6",
            "libpango-1.0-0",
            "libpangocairo-1.0-0",
            "libsm6",
            "libwayland-client0",
            "libwayland-cursor0",
            "libwayland-egl1",
            "libwayland-server0",
            "libx11-6",
            "libxcb1",
            "libxcomposite1",
            "libxcursor1",
            "libxdamage1",
            "libxext6",
            "libxfixes3",
            "libxi6",
            "libxinerama1",
            "libxrandr2",
            "libxrender1",
            "libxss1",
            "libxtst6",
        ]
        
        cmd = f"apt-get install -y -qq {' '.join(deps_to_install)}"
        run_command(ssh, cmd, "⏳ Instalando pacotes (pode levar alguns minutos)...", show_output=False)
        print("✅ Dependências instaladas")
        
        # 3. Reinstalar Playwright com dependências
        print("\n🔄 Reinstalando Playwright...")
        run_command(ssh, "cd /opt/smindeck-bot && python3 -m pip install --upgrade playwright -q", show_output=False)
        print("✅ Playwright atualizado")
        
        # 4. Instalar navegadores do Playwright
        print("\n🌐 Instalando navegadores do Playwright...")
        run_command(ssh, "python3 -m playwright install chromium --with-deps", "⏳ Instalando Chromium...")
        print("✅ Chromium instalado")
        
        # 5. Reiniciar bot
        print("\n🤖 Reiniciando bot...")
        run_command(ssh, "systemctl restart smindeck-bot", show_output=False)
        time.sleep(2)
        print("✅ Bot reiniciado")
        
        # 6. Verificar status
        print("\n📊 Verificando status...")
        stdin, stdout, stderr = ssh.exec_command("systemctl status smindeck-bot --no-pager | head -10")
        status = stdout.read().decode('utf-8', errors='replace')
        print(status)
        
        # 7. Ver logs recentes
        print("\n📋 Verificando logs...")
        stdin, stdout, stderr = ssh.exec_command("tail -10 /opt/smindeck-bot/debug.log")
        logs = stdout.read().decode('utf-8', errors='replace')
        print(logs)
        
    finally:
        ssh.close()
        print("\n✅ Processo concluído!")

if __name__ == "__main__":
    try:
        fix_dependencies()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
