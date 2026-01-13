#!/usr/bin/env python3
"""
Script para fazer deploy do bot.py no VPS com garantia de atualização
"""
import paramiko
import time
import sys

HOST = '72.60.244.240'
USER = 'root'
PASSWORD = 'Amor180725###'
REMOTE_PATH = '/opt/smindeck-bot/bot.py'
LOCAL_PATH = r'c:\Users\SAMUEL\Desktop\Smin-DECK virtual\bot.py'

def deploy():
    print("🚀 Iniciando deploy do bot.py...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(HOST, username=USER, password=PASSWORD)
        print(f"✅ Conectado ao VPS {HOST}")
        
        # 1️⃣ Matar processo anterior
        print("\n1️⃣ Matando bot anterior...")
        ssh.exec_command('pkill -9 -f "python3 bot.py"')
        time.sleep(1)
        
        # 2️⃣ Remover arquivo antigo
        print("2️⃣ Removendo arquivo antigo...")
        ssh.exec_command(f'rm -f {REMOTE_PATH}')
        time.sleep(0.5)
        
        # 3️⃣ Enviar novo arquivo
        print(f"3️⃣ Enviando novo bot.py...")
        sftp = ssh.open_sftp()
        sftp.put(LOCAL_PATH, REMOTE_PATH)
        sftp.close()
        print("   ✅ Arquivo enviado")
        
        # 4️⃣ Definir permissões
        print("4️⃣ Definindo permissões...")
        ssh.exec_command(f'chmod 755 {REMOTE_PATH}')
        
        # 5️⃣ Reiniciar serviço
        print("5️⃣ Reiniciando serviço via systemd...")
        ssh.exec_command('systemctl restart smindeck-bot')
        time.sleep(2)
        
        # 6️⃣ Verificar status
        print("6️⃣ Verificando status...")
        stdin, stdout, stderr = ssh.exec_command('systemctl is-active smindeck-bot')
        status = stdout.read().decode().strip()
        
        if status == 'active':
            print("   ✅ Serviço está ativo!")
        else:
            print(f"   ⚠️ Status: {status}")
        
        # 7️⃣ Verificar arquivo
        stdin, stdout, stderr = ssh.exec_command(f'ls -lh {REMOTE_PATH}')
        print(f"7️⃣ Arquivo no VPS:")
        print(f"   {stdout.read().decode().strip()}")
        
        # 8️⃣ Verificar conteúdo
        stdin, stdout, stderr = ssh.exec_command('grep -c "await mostrar_menu_principal" /opt/smindeck-bot/bot.py')
        count = stdout.read().decode().strip()
        print(f"\n✅ Deploy concluído!")
        print(f"✅ Linhas com 'mostrar_menu_principal': {count}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    finally:
        ssh.close()
    
    return True

if __name__ == "__main__":
    success = deploy()
    sys.exit(0 if success else 1)
