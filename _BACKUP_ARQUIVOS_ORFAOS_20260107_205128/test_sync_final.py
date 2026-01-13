#!/usr/bin/env python3
"""
Teste final da sincronização
"""
import paramiko
import time

VPS_HOST = "72.60.244.240"
VPS_USER = "root"
VPS_PASSWORD = "Amor180725###"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print("=" * 70)
print("🔍 TESTE FINAL DE SINCRONIZAÇÃO")
print("=" * 70)

print("\n1️⃣ Conectando ao VPS...")
ssh.connect(VPS_HOST, username=VPS_USER, password=VPS_PASSWORD, timeout=15)
print("✅ Conectado!")

print("\n2️⃣ Verificando API...")
stdin, stdout, stderr = ssh.exec_command('curl -s http://localhost:5001/api/health')
result = stdout.read().decode()
if 'ok' in result:
    print("✅ API respondendo")
else:
    print(f"❌ Erro: {result}")
    ssh.close()
    exit(1)

print("\n3️⃣ Verificando arquivos na pasta uploads...")
stdin, stdout, stderr = ssh.exec_command('ls -lh /opt/smindeck-bot/uploads/')
files = stdout.read().decode()
print(files)

print("\n4️⃣ Testando download de arquivo...")
stdin, stdout, stderr = ssh.exec_command('curl -s -o /tmp/test.bin http://localhost:5001/api/arquivo/video_botao_7.bin && ls -lh /tmp/test.bin')
result = stdout.read().decode()
if '/tmp/test.bin' in result:
    print(f"✅ Arquivo downloadado: {result.strip()}")
else:
    print(f"❌ Erro no download")
    print(stderr.read().decode())

print("\n5️⃣ Verificando status do Bot...")
stdin, stdout, stderr = ssh.exec_command('systemctl status smindeck-bot.service --no-pager | head -15')
status = stdout.read().decode()
print(status)

print("\n" + "=" * 70)
print("✅ SINCRONIZAÇÃO AGORA DEVE ESTAR FUNCIONANDO!")
print("=" * 70)
print("\n📝 Próximos passos:")
print("1. Abra a aplicação Windows")
print("2. Verifique se os videos/imagens aparecem nos botões")
print("3. Se não aparecer, aguarde 30 segundos (sync a cada 5 segundos)")
print("\n" + "=" * 70)

ssh.close()
