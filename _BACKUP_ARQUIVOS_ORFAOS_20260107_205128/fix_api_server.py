#!/usr/bin/env python3
"""
Script para criar e iniciar o serviço da API no VPS
Usa paramiko (SSH em Python puro)
"""

import paramiko
import sys
import time

# Credenciais
HOST = "72.60.244.240"
USER = "root"
PASSWORD = "Amor180725###"
PORT = 22

def ssh_exec(host, user, password, command):
    """Executa comando via SSH com paramiko"""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=PORT, username=user, password=password, timeout=10)
        
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8', errors='replace')
        error = stderr.read().decode('utf-8', errors='replace')
        
        ssh.close()
        return output, error
    except Exception as e:
        print(f"❌ Erro SSH: {e}")
        return None, str(e)

print("=" * 70)
print("🚀 CRIANDO SERVIÇO DA API NO VPS")
print("=" * 70)

# 1. Criar arquivo de serviço
print("\n📝 Etapa 1: Criando arquivo de serviço systemd...")
service_content = """[Unit]
Description=SminDeck API Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/smindeck-bot
ExecStart=/usr/bin/python3 /opt/smindeck-bot/api_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""

# Escrever arquivo diretamente
cmd1 = f"""tee /etc/systemd/system/smindeck-api.service > /dev/null << 'EOF'
{service_content}
EOF"""

output, error = ssh_exec(HOST, USER, PASSWORD, cmd1)
if output or not error:
    print("✅ Arquivo de serviço criado")
else:
    print(f"❌ Erro: {error}")

# 2. Recarregar systemd
print("\n🔄 Etapa 2: Recarregando systemd...")
output, error = ssh_exec(HOST, USER, PASSWORD, "systemctl daemon-reload")
if not error:
    print("✅ systemd recarregado")
else:
    print(f"⚠️ Aviso: {error}")

# 3. Habilitar serviço
print("\n✔️ Etapa 3: Habilitando serviço...")
output, error = ssh_exec(HOST, USER, PASSWORD, "systemctl enable smindeck-api.service")
if not error:
    print("✅ Serviço habilitado")
else:
    print(f"⚠️ Aviso: {error}")

# 4. Iniciar serviço
print("\n▶️ Etapa 4: Iniciando serviço API...")
output, error = ssh_exec(HOST, USER, PASSWORD, "systemctl start smindeck-api.service")
if not error:
    print("✅ Serviço iniciado")
else:
    print(f"⚠️ Aviso: {error}")

# 5. Aguardar inicialização
print("\n⏳ Aguardando 5 segundos para API inicializar...")
time.sleep(5)

# 6. Verificar status
print("\n📊 Etapa 5: Verificando status...")
output, error = ssh_exec(HOST, USER, PASSWORD, "systemctl status smindeck-api.service")
if output:
    # Pegar apenas primeira linha com resumo
    first_line = output.split('\n')[0]
    print(f"Status: {first_line}")
    if "active (running)" in output:
        print("✅ API está rodando!")
    elif "activating" in output:
        print("⏳ API ainda está iniciando...")
    else:
        print("⚠️ Status desconhecido")
        print(output[:300])

# 7. Testar API
print("\n🧪 Etapa 6: Testando endpoint da API...")
output, error = ssh_exec(HOST, USER, PASSWORD, "curl -s http://localhost:5001/api/health")
if output:
    print(f"✅ Resposta da API: {output}")
else:
    print(f"⚠️ Sem resposta ainda (pode estar iniciando): {error}")

# 8. Listar arquivos em uploads
print("\n📂 Etapa 7: Verificando arquivos em uploads/...")
output, error = ssh_exec(HOST, USER, PASSWORD, "ls -lh /opt/smindeck-bot/uploads/")
if output:
    print(output)

print("\n" + "=" * 70)
print("✅ CONCLUSÃO")
print("=" * 70)
print("A API foi configurada e iniciada!")
print("Aguarde 10 segundos e teste em sua app Windows.")
print("\nOu execute: python check_logs.py")
