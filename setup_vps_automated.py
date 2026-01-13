"""
Deploy Automático para VPS do Bot
Copia arquivos e inicia servidor de updates
"""

import os
import subprocess
import sys
from pathlib import Path

VPS_IP = "72.60.244.240"
VPS_USER = "root"
VPS_PORT = 22

def run_ssh_command(command):
    """Executa comando via SSH no VPS"""
    try:
        cmd = f'ssh -o StrictHostKeyChecking=no {VPS_USER}@{VPS_IP} "{command}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def copy_to_vps(local_file, remote_path):
    """Copia arquivo para VPS"""
    try:
        cmd = f'scp -o StrictHostKeyChecking=no "{local_file}" {VPS_USER}@{VPS_IP}:{remote_path}'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erro ao copiar: {e}")
        return False

def setup_vps():
    """Setup completo no VPS"""
    print("🚀 Iniciando setup do servidor de updates no VPS do Bot...")
    
    files_to_copy = [
        ("vps_update_server.py", "/root/vps_update_server.py"),
    ]
    
    # Criar diretório
    print("📁 Criando diretório de updates...")
    success, out, err = run_ssh_command("mkdir -p /root/smin_deck_updates && chmod 777 /root/smin_deck_updates")
    if success:
        print("✅ Diretório criado")
    else:
        print(f"⚠️ Erro: {err}")
    
    # Copiar arquivos
    for local, remote in files_to_copy:
        if os.path.exists(local):
            print(f"📤 Copiando {local}...")
            if copy_to_vps(local, remote):
                print(f"✅ {local} copiado")
            else:
                print(f"❌ Erro ao copiar {local}")
        else:
            print(f"❌ Arquivo não encontrado: {local}")
    
    # Instalar dependências
    print("📦 Instalando dependências...")
    success, out, err = run_ssh_command("pip3 install flask requests -q 2>/dev/null && echo 'OK'")
    if success and "OK" in out:
        print("✅ Dependências instaladas")
    else:
        print("⚠️ Erro ao instalar dependências")
    
    # Parar servidor anterior se houver
    print("🛑 Parando servidor anterior...")
    run_ssh_command("pkill -f vps_update_server.py 2>/dev/null || true")
    
    # Iniciar servidor em background
    print("🚀 Iniciando servidor de updates...")
    success, out, err = run_ssh_command("nohup python3 /root/vps_update_server.py > /root/updates_server.log 2>&1 &")
    
    # Esperar um pouco para servidor iniciar
    import time
    time.sleep(3)
    
    # Testar se está rodando
    print("🧪 Testando servidor...")
    success, out, err = run_ssh_command("curl -s http://localhost:8000/health | head -1")
    if success and "ok" in out.lower():
        print("✅ Servidor rodando!")
        print(f"   Endpoint: http://72.60.244.240:8001/api/updates/check")
        return True
    else:
        print("⚠️ Servidor pode estar inicializando, verificar logs:")
        success, logs, err = run_ssh_command("tail -20 /root/updates_server.log")
        print(logs)
        return False

if __name__ == "__main__":
    success = setup_vps()
    sys.exit(0 if success else 1)
