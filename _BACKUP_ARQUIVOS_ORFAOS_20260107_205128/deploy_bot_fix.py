#!/usr/bin/env python3
"""Copia bot.py corrigido para o VPS e reinicia o serviço"""

import paramiko
import os

# Ler arquivo local
with open('bot.py', 'r', encoding='utf-8') as f:
    bot_content = f.read()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("Conectando ao VPS...")
    vps_pass = os.environ.get('SMIN_VPS_PASS')
    if not vps_pass:
        raise RuntimeError('Defina a senha em SMIN_VPS_PASS (env var) antes de rodar este script.')

    ssh.connect('72.60.244.240', username='root', password=vps_pass, timeout=10)
    print("✅ Conectado!")
    
    # Usar SFTP para copiar arquivo
    sftp = ssh.open_sftp()
    
    # Garantir diretório (e permissões) no VPS
    ssh.exec_command('mkdir -p /opt/smindeck-bot')

    print("Enviando bot.py para o VPS...")
    sftp.putfo(open('bot.py', 'rb'), '/opt/smindeck-bot/bot.py')
    print("✅ Arquivo enviado!")
    
    sftp.close()
    
    # Reiniciar o serviço
    print("Reiniciando o serviço smindeck-bot...")
    stdin, stdout, stderr = ssh.exec_command('systemctl restart smindeck-bot')
    stdout.read()
    
    # Verificar status
    import time
    time.sleep(2)
    
    stdin, stdout, stderr = ssh.exec_command('systemctl status smindeck-bot --no-pager')
    status = stdout.read().decode()
    
    if 'active (running)' in status:
        print("✅ Bot reiniciado com sucesso!")
        print("\nStatus:")
        print(status[:300])
    else:
        print("⚠️ Verificar status:")
        print(status[:300])
    
    ssh.close()
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
