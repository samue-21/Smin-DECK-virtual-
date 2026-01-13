#!/usr/bin/env python3
import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='72.60.244.240', username='root', password='Amor180725###', port=22)

# Ver processos
print("=" * 50)
print("PROCESSOS PYTHON RODANDO:")
print("=" * 50)
stdin, stdout, stderr = ssh.exec_command('ps aux | grep python3 | grep -v grep')
procs = stdout.read().decode()
print(procs if procs.strip() else "❌ Nenhum processo encontrado")

# Ver banco
print("\n" + "=" * 50)
print("BANCO DE DADOS:")
print("=" * 50)
stdin, stdout, stderr = ssh.exec_command('ls -lah ~/.smindeckbot/')
print(stdout.read().decode())

# Ver logs
print("\n" + "=" * 50)
print("ÚLTIMOS LOGS:")
print("=" * 50)
stdin, stdout, stderr = ssh.exec_command('tail -50 /opt/smindeck-bot/debug.log')
logs = stdout.read().decode()
print(logs if logs.strip() else "❌ Sem logs")

ssh.close()
