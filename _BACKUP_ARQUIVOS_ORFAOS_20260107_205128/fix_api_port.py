#!/usr/bin/env python3
import paramiko

VPS_HOST = "72.60.244.240"
VPS_USER = "root"
VPS_PASSWORD = "Amor180725###"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("Conectando...")
ssh.connect(VPS_HOST, username=VPS_USER, password=VPS_PASSWORD, timeout=15)

print("Matando processo na porta 5001...")
stdin, stdout, stderr = ssh.exec_command('lsof -i :5001 2>/dev/null | grep -v COMMAND | awk "{print $2}" | xargs kill -9 2>/dev/null || true')
stdout.read()
stderr.read()

print("Parando serviço...")
stdin, stdout, stderr = ssh.exec_command('systemctl stop smindeck-api.service')
stdout.read()
stderr.read()

import time
print("Aguardando 2 segundos...")
time.sleep(2)

print("Iniciando serviço...")
stdin, stdout, stderr = ssh.exec_command('systemctl start smindeck-api.service')
stdout.read()
stderr.read()

print("Aguardando 3 segundos...")
time.sleep(3)

print("Testando...")
stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:5001/api/health')
result = stdout.read().decode()
print(f"Resposta: {result}")

if 'ok' in result:
    print("\n✅ API ativa e respondendo!")
else:
    print("\n❌ API ainda não está respondendo")
    print("\nVerificando status...")
    stdin, stdout, stderr = ssh.exec_command('systemctl status smindeck-api.service --no-pager')
    print(stdout.read().decode())

ssh.close()
