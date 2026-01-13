#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deploy automático para VPS com SSH via Paramiko
Copia os arquivos e executa comandos no VPS
"""

import paramiko
import sys
import os
from pathlib import Path

# Forçar UTF-8 no Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ⚠️ CREDENCIAIS
VPS_HOST = "72.60.244.240"
VPS_USER = "root"
VPS_PASSWORD = "Amor180725###"
VPS_PATH = "/opt/smindeck-bot/"

ARQUIVOS = [
    "arquivo_processor.py",
    "download_manager.py",
    "browser_downloader.py",
    "bot.py",
    "api_server.py",
    "sincronizador.py",
    "deck_window.py",
]

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))

def connect_ssh():
    """Conecta ao VPS via SSH"""
    print("🔐 Conectando ao VPS...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(VPS_HOST, username=VPS_USER, password=VPS_PASSWORD, timeout=10)
        print("✅ Conectado ao VPS!")
        return ssh
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        sys.exit(1)

def execute_command(ssh, cmd, description=""):
    """Executa comando no VPS"""
    if description:
        print(f"\n{description}")
    
    try:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        if error and "WARNING" not in error:
            print(f"⚠️  {error}")
            return False
        
        if output:
            print(output)
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def send_file(sftp, local_path, remote_path):
    """Envia arquivo via SFTP"""
    try:
        sftp.put(local_path, remote_path)
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar: {e}")
        return False

def deploy():
    """Deploy completo para o VPS"""
    
    print("\n" + "=" * 60)
    print("🚀 DEPLOY AUTOMÁTICO - SminDeck")
    print("=" * 60)
    
    # Conectar
    ssh = connect_ssh()
    sftp = ssh.open_sftp()
    
    try:
        # 1️⃣ ENVIAR ARQUIVOS
        print("\n" + "=" * 60)
        print("📤 ENVIANDO ARQUIVOS PARA VPS")
        print("=" * 60)
        
        for arquivo in ARQUIVOS:
            local = os.path.join(LOCAL_PATH, arquivo)
            remote = os.path.join(VPS_PATH, arquivo)
            
            if not os.path.exists(local):
                print(f"⚠️  {arquivo} não encontrado localmente, pulando...")
                continue
            
            print(f"\n📄 Enviando {arquivo}...")
            if send_file(sftp, local, remote):
                print(f"✅ {arquivo} enviado!")
            else:
                print(f"❌ Erro ao enviar {arquivo}")
                sys.exit(1)
        
        # 2️⃣ CRIAR PASTA UPLOADS
        print("\n" + "=" * 60)
        print("📁 CRIANDO ESTRUTURA DE PASTAS")
        print("=" * 60)
        
        execute_command(ssh, "mkdir -p /opt/smindeck-bot/uploads", "Criando pasta uploads...")
        print("✅ Pasta uploads criada!")
        
        # 3️⃣ INSTALAR DEPENDÊNCIAS
        print("\n" + "=" * 60)
        print("📦 INSTALANDO DEPENDÊNCIAS")
        print("=" * 60)
        
        execute_command(ssh, "apt update", "Atualizando pacotes...")
        print("✅ Pacotes atualizados!")
        
        execute_command(ssh, "apt install -y ffmpeg", "Instalando ffmpeg...")
        print("✅ ffmpeg instalado!")
        
        # Instalar TODAS as dependências do Playwright/Chromium
        deps = "libgbm1 libxss1 libasound2 libxkbcommon0 libx11-xcb1 libxrandr2 libxcb-dri3-0 libdrm-common libdrm2 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdbus-1-3 libdrm2 libgbm1 libpango-1.0-0 libpangocairo-1.0-0 libx11-6 libxcb1 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 libxrender1 libxkbcommon0 libpango1.0-0"
        execute_command(ssh, f"apt install -y {deps}", "Instalando dependências Playwright...")
        print("✅ Dependências do Playwright instaladas!")
        
        execute_command(ssh, "pip install --no-cache-dir Pillow aiohttp playwright", "Instalando Python packages...")
        print("✅ Python packages instalados!")
        
        # Instalar Chromium com ffmpeg
        execute_command(ssh, "python3 -m playwright install chromium", "Instalando Chromium...")
        print("✅ Chromium instalado!")
        
        # 4️⃣ VERIFICAR PERMISSÕES
        print("\n" + "=" * 60)
        print("🔐 AJUSTANDO PERMISSÕES")
        print("=" * 60)
        
        execute_command(ssh, "chmod 755 /opt/smindeck-bot/*.py && chmod 755 /opt/smindeck-bot/uploads", 
                       "Ajustando permissões...")
        print("✅ Permissões ajustadas!")
        
        # 5️⃣ CRIAR SERVIÇO DA API (se não existir)
        print("\n" + "=" * 60)
        print("⚙️  CRIANDO SERVIÇO DA API")
        print("=" * 60)
        
        # Criar o arquivo de serviço localmente
        import tempfile
        service_content = b'''[Unit]
Description=SminDeck API Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
User=root
WorkingDirectory=/opt/smindeck-bot
ExecStart=/usr/bin/python3 /opt/smindeck-bot/api_server.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
'''
        
        # Enviar arquivo de serviço via SFTP
        print("📝 Criando arquivo de serviço da API...")
        try:
            # Criar arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(service_content)
                tmp_path = tmp.name
            
            # Enviar para /tmp
            sftp.put(tmp_path, '/tmp/smindeck-api.service')
            os.unlink(tmp_path)
            
            # Mover para local correto
            execute_command(ssh, 'sudo mv /tmp/smindeck-api.service /etc/systemd/system/smindeck-api.service', 
                          "Movendo arquivo...")
            execute_command(ssh, 'sudo systemctl daemon-reload', "Recarregando systemd...")
            execute_command(ssh, 'sudo systemctl enable smindeck-api.service', "Habilitando serviço...")
            print("✅ Serviço da API criado!")
        except Exception as e:
            print(f"⚠️  Erro ao criar serviço: {e}")
        
        # 5️⃣ REINICIAR SERVIÇOS
        print("\n" + "=" * 60)
        print("🔄 REINICIANDO SERVIÇOS")
        print("=" * 60)
        
        execute_command(ssh, "systemctl restart smindeck-bot", "Reiniciando bot...")
        print("✅ Bot reiniciado!")
        
        execute_command(ssh, "systemctl restart smindeck-api.service", "Reiniciando API...")
        print("✅ API reiniciada!")
        
        # 6️⃣ VERIFICAR STATUS
        print("\n" + "=" * 60)
        print("✅ VERIFICANDO STATUS DOS SERVIÇOS")
        print("=" * 60)
        
        execute_command(ssh, "systemctl status smindeck-bot --no-pager", "Status do Bot:")
        execute_command(ssh, "systemctl status smindeck-api --no-pager", "Status da API:")
        
        # SUCESSO!
        print("\n" + "=" * 60)
        print("🎉 DEPLOY CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        print("\n📝 Próximos passos:")
        print("1. Abre o APP local")
        print("2. No Discord: envia 'oi'")
        print("3. Seleciona um botão (ex: Botão 5)")
        print("4. Seleciona 'Atualizar Vídeo' ou 'Atualizar Imagem'")
        print("5. Envia um arquivo (MP4, JPG, PNG, etc)")
        print("\n✅ O arquivo será automaticamente:")
        print("   • Processado e otimizado no VPS")
        print("   • Baixado pelo APP")
        print("   • Adicionado ao botão selecionado")
        print("   • Deletado do VPS")
        
        print("\n📊 Para ver logs em tempo real:")
        print("   ssh root@72.60.244.240")
        print("   tail -f /opt/smindeck-bot/debug.log")
        
    finally:
        sftp.close()
        ssh.close()
        print("\n✅ Conexão encerrada!")

if __name__ == "__main__":
    try:
        deploy()
    except KeyboardInterrupt:
        print("\n\n❌ Deploy cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
