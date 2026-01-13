#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Criar serviço systemd para a API
"""

import paramiko
import sys

VPS_HOST = "72.60.244.240"
VPS_USER = "root"
VPS_PASSWORD = "Amor180725###"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("🔐 Conectando ao VPS...")
ssh.connect(VPS_HOST, username=VPS_USER, password=VPS_PASSWORD)
print("✅ Conectado!")

# Criar o arquivo de serviço da API
service_content = '''[Unit]
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

print("\n📝 Criando arquivo de serviço...")
stdin, stdout, stderr = ssh.exec_command(
    'cat > /etc/systemd/system/smindeck-api.service',
    input=service_content.encode()
)
stdout.read()
err = stderr.read().decode()
if err:
    print(f"⚠️  {err}")

print("✅ Arquivo criado!")

print("\n🔄 Recarregando systemd...")
stdin, stdout, stderr = ssh.exec_command('systemctl daemon-reload')
stdout.read()
stderr.read()
print("✅ Recarregado!")

print("\n▶️  Iniciando serviço da API...")
stdin, stdout, stderr = ssh.exec_command('systemctl start smindeck-api.service')
stdout.read()
stderr.read()
print("✅ Iniciado!")

print("\n📌 Habilitando serviço...")
stdin, stdout, stderr = ssh.exec_command('systemctl enable smindeck-api.service')
stdout.read()
stderr.read()
print("✅ Habilitado!")

print("\n📊 Verificando status...")
stdin, stdout, stderr = ssh.exec_command('systemctl status smindeck-api.service --no-pager')
status = stdout.read().decode()
print(status)

print("\n🌐 Testando acesso à API...")
stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:5001/api/status || echo "API não respondeu"')
api_status = stdout.read().decode()
print(api_status)

ssh.close()
print("\n✅ Conexão encerrada!")
