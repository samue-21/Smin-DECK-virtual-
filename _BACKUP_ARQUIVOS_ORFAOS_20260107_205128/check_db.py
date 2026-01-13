#!/usr/bin/env python3
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='72.60.244.240', username='root', password='Amor180725###', port=22)

# Listar tabelas
stdin, stdout, stderr = ssh.exec_command('sqlite3 ~/.smindeckbot/smindeckbot.db ".tables"')
print('Tabelas:')
print(stdout.read().decode())

# Verificar tamanho
stdin, stdout, stderr = ssh.exec_command('ls -lah ~/.smindeckbot/smindeckbot.db')
print('Tamanho:')
print(stdout.read().decode())

# Ver schema
stdin, stdout, stderr = ssh.exec_command('sqlite3 ~/.smindeckbot/smindeckbot.db ".schema"')
print('Schema:')
print(stdout.read().decode())

ssh.close()
