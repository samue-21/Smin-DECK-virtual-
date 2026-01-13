#!/bin/bash

# 🤖 Script de Instalação do SminDeck Bot no VPS
# Copia bot.py, configura .env e inicia serviço permanente

set -e  # Parar se algum comando falhar

echo "=================================="
echo "🚀 Instalação SminDeck Bot no VPS"
echo "=================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Diretório de instalação
BOT_DIR="/opt/smindeck-bot"
BOT_USER="smindeck"
BOT_SERVICE="smindeck-bot"

echo -e "${YELLOW}Passo 1: Criar diretório e usuário${NC}"
# Criar diretório se não existir
if [ ! -d "$BOT_DIR" ]; then
    echo "📁 Criando diretório: $BOT_DIR"
    sudo mkdir -p $BOT_DIR
else
    echo "✅ Diretório já existe: $BOT_DIR"
fi

# Criar usuário se não existir
if ! id "$BOT_USER" &>/dev/null; then
    echo "👤 Criando usuário: $BOT_USER"
    sudo useradd -r -s /bin/bash $BOT_USER
else
    echo "✅ Usuário já existe: $BOT_USER"
fi

# Dar permissões
echo "🔑 Configurando permissões..."
sudo chown -R $BOT_USER:$BOT_USER $BOT_DIR
sudo chmod 755 $BOT_DIR

echo ""
echo -e "${YELLOW}Passo 2: Copiar arquivo bot.py${NC}"
if [ -f "bot.py" ]; then
    echo "📋 Copiando bot.py..."
    sudo cp bot.py $BOT_DIR/bot.py
    sudo chown $BOT_USER:$BOT_USER $BOT_DIR/bot.py
    echo "✅ bot.py copiado"
else
    echo -e "${RED}❌ Arquivo bot.py não encontrado!${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Passo 3: Configurar .env${NC}"
if [ ! -f "$BOT_DIR/.env" ]; then
    echo "📝 Criando arquivo .env..."
    
    # Ler token do usuário
    echo ""
    echo "Você tem o token do Discord Bot?"
    echo "Para obter:"
    echo "  1. Acesse: https://discord.com/developers/applications"
    echo "  2. Clique na sua aplicação"
    echo "  3. Vá em 'Bot'"
    echo "  4. Clique 'Copy' embaixo de TOKEN"
    echo ""
    read -p "Cole o token aqui: " DISCORD_TOKEN
    
    if [ -z "$DISCORD_TOKEN" ]; then
        echo -e "${RED}❌ Token não pode estar vazio!${NC}"
        exit 1
    fi
    
    # Criar arquivo .env
    echo "DISCORD_TOKEN=$DISCORD_TOKEN" | sudo tee $BOT_DIR/.env > /dev/null
    sudo chown $BOT_USER:$BOT_USER $BOT_DIR/.env
    sudo chmod 600 $BOT_DIR/.env  # Apenas o usuário pode ler
    
    echo "✅ Arquivo .env criado"
else
    echo "✅ Arquivo .env já existe"
fi

echo ""
echo -e "${YELLOW}Passo 4: Instalar dependências Python${NC}"

# Verificar se Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "⚠️ Python 3 não encontrado. Instalando..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
else
    echo "✅ Python 3 já instalado"
fi

# Instalar discord.py
echo "📦 Instalando discord.py..."
sudo pip3 install discord.py python-dotenv

echo "✅ Dependências instaladas"

echo ""
echo -e "${YELLOW}Passo 5: Criar serviço systemd${NC}"

SERVICE_FILE="/etc/systemd/system/${BOT_SERVICE}.service"

echo "📄 Criando arquivo: $SERVICE_FILE"

sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=SminDeck Discord Bot
After=network.target

[Service]
Type=simple
User=$BOT_USER
WorkingDirectory=$BOT_DIR
ExecStart=/usr/bin/python3 $BOT_DIR/bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Serviço criado"

echo ""
echo -e "${YELLOW}Passo 6: Habilitar e iniciar serviço${NC}"

# Recarregar systemd
sudo systemctl daemon-reload

# Habilitar serviço (iniciar automaticamente)
echo "🔄 Habilitando serviço..."
sudo systemctl enable $BOT_SERVICE

# Iniciar serviço
echo "🚀 Iniciando serviço..."
sudo systemctl start $BOT_SERVICE

# Aguardar um pouco para iniciar
sleep 2

# Verificar status
if sudo systemctl is-active --quiet $BOT_SERVICE; then
    echo -e "${GREEN}✅ Serviço iniciado com sucesso!${NC}"
else
    echo -e "${RED}⚠️ Verificando erro...${NC}"
    sudo systemctl status $BOT_SERVICE
fi

echo ""
echo "=================================="
echo -e "${GREEN}✅ Instalação Concluída!${NC}"
echo "=================================="
echo ""
echo "📊 Status do Bot:"
sudo systemctl status $BOT_SERVICE --no-pager

echo ""
echo "📋 Comandos úteis:"
echo "  Ver logs: sudo journalctl -u $BOT_SERVICE -f"
echo "  Parar bot: sudo systemctl stop $BOT_SERVICE"
echo "  Iniciar bot: sudo systemctl start $BOT_SERVICE"
echo "  Reiniciar bot: sudo systemctl restart $BOT_SERVICE"
echo ""

echo "🎉 Bot está rodando 24/7 no VPS!"
echo "O bot vai criar o canal #smindeck automaticamente quando for adicionado ao servidor."
