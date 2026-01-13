#!/usr/bin/env python3
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.60.244.240', username='root', password='Amor180725###')

# Parar o serviço
print("[1] Parando o servico smindeck-api...")
stdin, stdout, stderr = ssh.exec_command('systemctl stop smindeck-api.service')
out = stdout.read().decode()
err = stderr.read().decode()
if err:
    print(f"[WARNING] {err[:200]}")

# Matar processos Python na porta 5001
print("\n[2] Matando processos Python na porta 5001...")
stdin, stdout, stderr = ssh.exec_command('lsof -ti:5001 | xargs kill -9 2>/dev/null; echo "ok"')
print(stdout.read().decode()[:100])

# Aguardar
import time
print("\n[3] Aguardando 3 segundos...")
time.sleep(3)

# Reiniciar o serviço
print("\n[4] Reiniciando o servico...")
stdin, stdout, stderr = ssh.exec_command('systemctl start smindeck-api.service')
out = stdout.read().decode()
if out:
    print(f"[OK] {out[:100]}")

# Aguardar inicialização
print("\n[5] Aguardando 5 segundos para inicializar...")
time.sleep(5)

# Verificar status
print("\n[6] Verificando status...")
stdin, stdout, stderr = ssh.exec_command('systemctl status smindeck-api.service | head -5')
print(stdout.read().decode())

# Testar API
print("\n[7] Testando API...")
stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:5001/api/health')
result = stdout.read().decode()
print(f"Resultado: {result}")

# Testar download de arquivo
print("\n[8] Testando download de arquivo...")
stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:5001/api/arquivo/video_botao_7.bin | head -c 100')
result = stdout.read().decode()
print(f"Resultado: {result[:100]}")

ssh.close()
print("\n[OK] Tudo pronto!")
