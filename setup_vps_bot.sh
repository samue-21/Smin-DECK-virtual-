#!/bin/bash
# Script de setup do servidor de updates no VPS do Bot
# Execute como root no VPS

echo "🚀 Configurando servidor de updates Smin-DECK no VPS do Bot..."

# Criar diretório
mkdir -p /root/smin_deck_updates
chmod 777 /root/smin_deck_updates

# Instalar dependências
pip3 install flask requests

# Copiar arquivo do servidor
# (você precisa fazer scp vps_update_server.py root@VPS_IP:/root/)

# Criar serviço systemd
cat > /etc/systemd/system/smin-updates.service << EOF
[Unit]
Description=Smin-DECK Updates Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root
ExecStart=/usr/bin/python3 /root/vps_update_server.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Habilitar e iniciar serviço
systemctl daemon-reload
systemctl enable smin-updates.service
systemctl start smin-updates.service

echo "✅ Servidor de updates iniciado!"
echo "Status: systemctl status smin-updates"
echo "Logs: journalctl -u smin-updates -f"
