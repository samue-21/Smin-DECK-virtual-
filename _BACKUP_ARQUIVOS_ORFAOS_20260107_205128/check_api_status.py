#!/usr/bin/env python3
import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.60.244.240', username='root', password='Amor180725###', timeout=10)

# Ver status
stdin, stdout, stderr = ssh.exec_command('systemctl status smindeck-api.service')
print("=== STATUS ===")
print(stdout.read().decode()[:500])

# Ver logs
stdin, stdout, stderr = ssh.exec_command('journalctl -u smindeck-api.service -n 20')
print("\n=== LOGS ===")
print(stdout.read().decode())

# Testar curl local
stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:5001/api/arquivo/video_botao_7.bin')
print("\n=== TESTE CURL ===")
print(stdout.read().decode())

ssh.close()
