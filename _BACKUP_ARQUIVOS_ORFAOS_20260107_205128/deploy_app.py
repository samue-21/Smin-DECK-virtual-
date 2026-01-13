#!/usr/bin/env python3
"""
Deploy do APP - Envia arquivos modificados para o VPS
"""
import os
import paramiko

VPS_IP = '72.60.244.240'
VPS_USER = 'root'
VPS_PASSWORD = 'Amor180725###'
APP_DIR = '/opt/smindeck-app'  # Diretório no VPS para app files

# Arquivos a sincronizar
FILES_TO_SYNC = [
    'sincronizador.py',
    'deck_window.py'
]

def deploy_app_files():
    """Envia arquivos do app para a VPS"""
    print("🚀 Iniciando deploy do APP...")
    
    try:
        # Conectar SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(VPS_IP, username=VPS_USER, password=VPS_PASSWORD, timeout=10)
        print(f"✅ Conectado ao VPS {VPS_IP}\n")
        
        sftp = ssh.open_sftp()
        
        for filename in FILES_TO_SYNC:
            local_path = os.path.join(os.path.dirname(__file__), filename)
            
            if not os.path.exists(local_path):
                print(f"⚠️  Arquivo não encontrado: {local_path}")
                continue
            
            # Enviar para VPS em pasta temporária (usuário pode sincronizar manualmente)
            remote_path = f'/tmp/{filename}.new'
            print(f"📤 Enviando {filename}...")
            sftp.put(local_path, remote_path)
            print(f"   ✅ Enviado para {remote_path}")
            print(f"      (Lembre-se: O app lerá daqui no próximo sync)")
        
        sftp.close()
        ssh.close()
        
        print("\n✅ Deploy do app concluído!")
        print("   Os arquivos estão prontos para o app sincronizar.")
        
    except Exception as e:
        print(f"❌ ERRO no deploy: {e}")
        return False
    
    return True

if __name__ == '__main__':
    deploy_app_files()
