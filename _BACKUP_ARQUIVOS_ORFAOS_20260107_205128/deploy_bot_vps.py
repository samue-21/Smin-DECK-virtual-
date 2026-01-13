#!/usr/bin/env python3
"""
Script para instalar o bot no VPS via SSH
Envia bot.py, cria .env e inicia o serviço
"""

import subprocess
import sys
import os
from pathlib import Path

# Configuração
VPS_IP = "72.60.244.240"
VPS_USER = "root"  # Ou o usuário que você usa
BOT_DIR = "/opt/smindeck-bot"

def run_command(cmd, description=""):
    """Executar comando e mostrar resultado"""
    if description:
        print(f"\n📋 {description}")
    
    print(f"▶️  {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Sucesso")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ Erro:")
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    return True


def main():
    print("="*50)
    print("🚀 Instalador SminDeck Bot - VPS")
    print(f"VPS: {VPS_IP}")
    print("="*50)
    
    # Verificar se bot.py existe
    if not Path("bot.py").exists():
        print("❌ Arquivo bot.py não encontrado!")
        print("Certifique-se de estar no diretório correto.")
        sys.exit(1)
    
    # Passo 1: Copiar bot.py
    print("\n" + "="*50)
    print("Passo 1: Copiar bot.py para VPS")
    print("="*50)
    
    cmd = f'scp -P 22 bot.py {VPS_USER}@{VPS_IP}:{BOT_DIR}/'
    if not run_command(cmd, "Enviando bot.py..."):
        print("⚠️  Falha ao enviar bot.py")
        print("Você tem SSH configurado?")
        sys.exit(1)
    
    # Passo 2: Executar script de instalação
    print("\n" + "="*50)
    print("Passo 2: Executar script de instalação")
    print("="*50)
    
    cmd = f'''ssh -p 22 {VPS_USER}@{VPS_IP} << 'ENDSSH'
#!/bin/bash
set -e

BOT_DIR="/opt/smindeck-bot"
BOT_USER="smindeck"

echo "📁 Criando diretório..."
mkdir -p $BOT_DIR

echo "👤 Criando usuário..."
useradd -r -s /bin/bash smindeck 2>/dev/null || true

echo "🔑 Configurando permissões..."
chown -R $BOT_USER:$BOT_USER $BOT_DIR
chmod 755 $BOT_DIR

echo "📦 Instalando Python..."
apt-get update -qq
apt-get install -qq -y python3 python3-pip

echo "📚 Instalando dependências..."
pip3 install -q discord.py python-dotenv

echo "📝 Criando .env..."
read -p "Cole seu DISCORD_TOKEN: " TOKEN
echo "DISCORD_TOKEN=$TOKEN" > $BOT_DIR/.env
chmod 600 $BOT_DIR/.env
chown $BOT_USER:$BOT_USER $BOT_DIR/.env

echo "📄 Criando serviço systemd..."
tee /etc/systemd/system/smindeck-bot.service > /dev/null << 'EOF'
[Unit]
Description=SminDeck Discord Bot
After=network.target

[Service]
Type=simple
User=smindeck
WorkingDirectory=/opt/smindeck-bot
ExecStart=/usr/bin/python3 /opt/smindeck-bot/bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo "🚀 Iniciando serviço..."
systemctl daemon-reload
systemctl enable smindeck-bot
systemctl start smindeck-bot

sleep 2

echo "✅ Bot iniciado!"
systemctl status smindeck-bot --no-pager

ENDSSH
'''
    
    if not run_command(cmd, "Executando instalação no VPS..."):
        print("⚠️  Houve um erro durante a instalação")
        print("Verifique a conexão SSH e tente novamente")
        sys.exit(1)
    
    # Passo 3: Verificar status
    print("\n" + "="*50)
    print("Verificando status do bot")
    print("="*50)
    
    cmd = f'ssh -p 22 {VPS_USER}@{VPS_IP} "systemctl status smindeck-bot --no-pager"'
    run_command(cmd)
    
    print("\n" + "="*50)
    print("✅ INSTALAÇÃO CONCLUÍDA!")
    print("="*50)
    print(f"""
🎉 Bot está rodando no VPS: {VPS_IP}

📊 Comandos úteis:
  Ver logs:    ssh {VPS_USER}@{VPS_IP} journalctl -u smindeck-bot -f
  Parar:       ssh {VPS_USER}@{VPS_IP} systemctl stop smindeck-bot
  Iniciar:     ssh {VPS_USER}@{VPS_IP} systemctl start smindeck-bot
  Reiniciar:   ssh {VPS_USER}@{VPS_IP} systemctl restart smindeck-bot

🤖 Bot vai estar sempre online e criar canais automaticamente!
""")


if __name__ == "__main__":
    main()
