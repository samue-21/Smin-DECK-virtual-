#!/usr/bin/env python3
import paramiko
import sys

VPS_HOST = "72.60.244.240"
VPS_USER = "root"
VPS_PASSWORD = "Amor180725###"

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print("🔐 Conectando...")
    ssh.connect(VPS_HOST, username=VPS_USER, password=VPS_PASSWORD, timeout=10)
    print("✅ Conectado!")
    
    # Verificar se api_server.py existe
    stdin, stdout, stderr = ssh.exec_command('ls -la /opt/smindeck-bot/api_server.py')
    result = stdout.read().decode()
    print(f"\n📁 Arquivo:\n{result}")
    
    # Verificar se serviço existe
    stdin, stdout, stderr = ssh.exec_command('ls -la /etc/systemd/system/smindeck-api.service 2>&1')
    result = stdout.read().decode()
    err = stderr.read().decode()
    print(f"\n⚙️  Serviço:\n{result}{err}")
    
    # Criar serviço
    print("\n📝 Criando serviço...")
    cmd = '''cat > /etc/systemd/system/smindeck-api.service << 'EOF'
[Unit]
Description=SminDeck API Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/smindeck-bot
ExecStart=/usr/bin/python3 /opt/smindeck-bot/api_server.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF'''
    
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.read()
    err = stderr.read().decode()
    if err:
        print(f"Erro: {err}")
    else:
        print("✅ Arquivo criado!")
    
    # Reload systemd
    print("🔄 Recarregando...")
    stdin, stdout, stderr = ssh.exec_command('systemctl daemon-reload')
    stdout.read()
    stderr.read()
    print("✅ Recarregado!")
    
    # Iniciar
    print("▶️  Iniciando...")
    stdin, stdout, stderr = ssh.exec_command('systemctl restart smindeck-api')
    stdout.read()
    err = stderr.read().decode()
    if err:
        print(f"Aviso: {err}")
    print("✅ Iniciado!")
    
    # Status
    stdin, stdout, stderr = ssh.exec_command('systemctl status smindeck-api --no-pager')
    status = stdout.read().decode()
    print(f"\n📊 Status:\n{status}")
    
    ssh.close()
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
