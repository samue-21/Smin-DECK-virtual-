#!/usr/bin/env python3
import paramiko

VPS_HOST = "72.60.244.240"
VPS_USER = "root"
VPS_PASSWORD = "Amor180725###"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("Conectando...")
ssh.connect(VPS_HOST, username=VPS_USER, password=VPS_PASSWORD, timeout=15)

print("Testando se API está rodando...")
stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:5001/api/health')
result = stdout.read().decode()
print(f"Resposta: {result}")

if 'ok' not in result:
    print("\n❌ API não está respondendo!")
    print("\nVerificando processo...")
    stdin, stdout, stderr = ssh.exec_command('ps aux | grep api_server')
    print(stdout.read().decode())
    
    print("\nVerificando porta 5001...")
    stdin, stdout, stderr = ssh.exec_command('netstat -tlnp | grep 5001')
    print(stdout.read().decode())

ssh.close()
