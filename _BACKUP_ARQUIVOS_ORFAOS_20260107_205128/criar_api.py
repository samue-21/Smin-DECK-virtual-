#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Criar e iniciar serviço da API no VPS
"""

import paramiko
import tempfile
import os

VPS_HOST = "72.60.244.240"
VPS_USER = "root"
VPS_PASSWORD = "Amor180725###"

print("🔐 Conectando ao VPS...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(VPS_HOST, username=VPS_USER, password=VPS_PASSWORD)

sftp = ssh.open_sftp()

# Conteúdo do serviço
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

# Criar arquivo temporário
with tempfile.NamedTemporaryFile(delete=False, suffix='.service') as tmp:
    tmp.write(service_content)
    tmp_path = tmp.name

try:
    print("📤 Enviando arquivo de serviço...")
    sftp.put(tmp_path, '/tmp/smindeck-api.service')
    
    print("📝 Movendo para /etc/systemd/system/...")
    stdin, stdout, stderr = ssh.exec_command('mv /tmp/smindeck-api.service /etc/systemd/system/smindeck-api.service')
    stdout.read()
    stderr.read()
    
    print("🔄 Recarregando systemd...")
    stdin, stdout, stderr = ssh.exec_command('systemctl daemon-reload')
    stdout.read()
    stderr.read()
    
    print("⚙️  Habilitando serviço...")
    stdin, stdout, stderr = ssh.exec_command('systemctl enable smindeck-api.service')
    stdout.read()
    stderr.read()
    
    print("▶️  Iniciando serviço...")
    stdin, stdout, stderr = ssh.exec_command('systemctl start smindeck-api.service')
    stdout.read()
    stderr.read()
    
    print("\n📊 Status da API:")
    stdin, stdout, stderr = ssh.exec_command('systemctl status smindeck-api.service --no-pager')
    print(stdout.read().decode())
    
    print("\n✅ Serviço criado e iniciado com sucesso!")
    
finally:
    os.unlink(tmp_path)
    sftp.close()
    ssh.close()
