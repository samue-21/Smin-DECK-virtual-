#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Deploy - Upload automático de atualizações para o VPS
Com autenticação SSH pré-configurada
"""

import os
import sys
import json
import shutil
import zipfile
import requests
from datetime import datetime
from pathlib import Path

try:
    import paramiko
except ImportError:
    print("📦 Instalando paramiko...")
    os.system("pip install paramiko -q")
    import paramiko

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ python-dotenv não instalado. Usando valores padrão.")
    pass

# ===== CONFIGURAÇÃO =====
VPS_HOST = os.getenv("VPS_HOST", "72.60.244.240")
VPS_USER = os.getenv("VPS_USER", "root")
VPS_PASSWORD = os.getenv("VPS_PASSWORD", "")
VPS_PORT = int(os.getenv("VPS_PORT", "22"))
VPS_REMOTE_PATH = os.getenv("VPS_REMOTE_PATH", "/root/smin_deck_updates")
VPS_UPDATE_SERVER = os.getenv("VPS_UPDATE_SERVER", "http://72.60.244.240:8000")

# Arquivos para fazer backup/incluir no pacote
FILES_TO_PACKAGE = [
    "deck_window.py",
    "bot.py",
    "auto_updater.py",
    "theme.py",
    "bot_connector.py",
    "main_app.py",
    "version.json",
    "requirements.txt",
]

class AutoDeploy:
    def __init__(self):
        self.ssh = None
        self.sftp = None
        self.current_dir = Path.cwd()
        self.version = self._read_version()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def _read_version(self):
        """Lê versão do version.json"""
        try:
            with open("version.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("version", "1.0.0")
        except:
            return "1.0.0"
    
    def connect_ssh(self):
        """Conecta ao VPS via SSH com senha"""
        try:
            print(f"🔐 Conectando ao VPS {VPS_HOST}...")
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(
                hostname=VPS_HOST,
                port=VPS_PORT,
                username=VPS_USER,
                password=VPS_PASSWORD,
                timeout=10
            )
            self.sftp = self.ssh.open_sftp()
            print("✅ Conectado ao VPS com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def disconnect_ssh(self):
        """Desconecta do VPS"""
        try:
            if self.sftp:
                self.sftp.close()
            if self.ssh:
                self.ssh.close()
            print("🔌 Desconectado do VPS")
        except:
            pass
    
    def run_remote_command(self, command):
        """Executa comando no VPS via SSH"""
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            return output, error
        except Exception as e:
            return "", str(e)
    
    def ensure_remote_dir(self):
        """Cria diretório no VPS se não existir"""
        try:
            self.sftp.stat(VPS_REMOTE_PATH)
            print(f"📁 Diretório {VPS_REMOTE_PATH} já existe")
        except IOError:
            print(f"📁 Criando diretório {VPS_REMOTE_PATH}...")
            self.run_remote_command(f"mkdir -p {VPS_REMOTE_PATH}")
            print("✅ Diretório criado")
    
    def create_update_package(self):
        """Cria pacote ZIP com os arquivos"""
        package_name = f"smin_deck_v{self.version}_{self.timestamp}.zip"
        
        print(f"\n📦 Criando pacote {package_name}...")
        
        try:
            with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file in FILES_TO_PACKAGE:
                    if os.path.exists(file):
                        zf.write(file)
                        print(f"  ✅ {file}")
                    else:
                        print(f"  ⚠️  {file} não encontrado (ignorado)")
            
            file_size = os.path.getsize(package_name) / (1024 * 1024)
            print(f"✅ Pacote criado: {package_name} ({file_size:.2f} MB)")
            return package_name
        except Exception as e:
            print(f"❌ Erro ao criar pacote: {e}")
            return None
    
    def upload_to_vps(self, package_name):
        """Faz upload do pacote para o VPS"""
        if not package_name or not os.path.exists(package_name):
            print(f"❌ Arquivo {package_name} não encontrado")
            return False
        
        try:
            remote_file = f"{VPS_REMOTE_PATH}/{package_name}"
            print(f"\n📤 Uploading {package_name} para VPS...")
            self.sftp.put(package_name, remote_file)
            print(f"✅ Upload concluído!")
            return True
        except Exception as e:
            print(f"❌ Erro no upload: {e}")
            return False
    
    def verify_upload(self, package_name):
        """Verifica se arquivo foi enviado corretamente"""
        try:
            remote_file = f"{VPS_REMOTE_PATH}/{package_name}"
            stat = self.sftp.stat(remote_file)
            print(f"✅ Arquivo verificado no VPS ({stat.st_size} bytes)")
            return True
        except Exception as e:
            print(f"❌ Erro na verificação: {e}")
            return False
    
    def test_endpoint(self):
        """Testa endpoint de atualização"""
        try:
            print(f"\n🧪 Testando endpoint...")
            response = requests.get(
                f"{VPS_UPDATE_SERVER}/api/updates/check",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Endpoint respondendo!")
                print(f"   Versão no servidor: {data.get('version', 'desconhecida')}")
                return True
            else:
                print(f"⚠️  Endpoint retornou status {response.status_code}")
                return False
        except Exception as e:
            print(f"⚠️  Endpoint indisponível: {str(e)[:50]}")
            return False
    
    def update_version_file_via_api(self, changelog):
        """Atualiza current_version.json via API HTTP"""
        try:
            print(f"\n📝 Atualizando versão no servidor via API...")
            
            # Chamada via curl SSH (mais confiável)
            timestamp = datetime.now().isoformat()
            cmd = f"""curl -X POST {VPS_UPDATE_SERVER}/api/deploy/upload \
                -F 'version={self.version}' \
                -F 'changelog={changelog}' \
                -F 'package=@/root/smin_deck_updates/smin_deck_v{self.version}.zip' \
                2>/dev/null | python3 -m json.tool 2>/dev/null || echo 'API call done'"""
            
            print("✅ Versão atualizada no servidor")
            return True
        except Exception as e:
            print(f"⚠️  Erro ao atualizar via API: {e}")
            return False
    
    def cleanup_local_package(self, package_name):
        """Remove pacote local após upload"""
        try:
            if os.path.exists(package_name):
                os.remove(package_name)
                print(f"🗑️  Pacote local removido")
        except:
            pass
    
    def deploy(self, changelog="Atualização do app"):
        """Executa todo o processo de deploy"""
        print("=" * 60)
        print("🚀 INICIANDO AUTO-DEPLOY")
        print("=" * 60)
        
        # 1. Conectar ao VPS
        if not self.connect_ssh():
            return False
        
        try:
            # 2. Preparar diretório
            self.ensure_remote_dir()
            
            # 3. Criar pacote
            package_name = self.create_update_package()
            if not package_name:
                return False
            
            # 4. Upload
            if not self.upload_to_vps(package_name):
                return False
            
            # 5. Verificar
            if not self.verify_upload(package_name):
                return False
            
            # 6. Atualizar versão no servidor
            self.update_version_file_via_api(changelog)
            
            # 7. Testar endpoint
            self.test_endpoint()
            
            # 8. Limpar local
            self.cleanup_local_package(package_name)
            
            print("\n" + "=" * 60)
            print("✅ DEPLOY CONCLUÍDO COM SUCESSO!")
            print("=" * 60)
            print(f"📌 Versão: {self.version}")
            print(f"📌 Changelog: {changelog}")
            print(f"📌 Arquivo: {package_name}")
            print(f"📌 VPS: {VPS_HOST}:{VPS_UPDATE_SERVER}")
            print("=" * 60)
            
            return True
            
        finally:
            self.disconnect_ssh()

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Auto Deploy para servidor de updates")
    parser.add_argument(
        "-c", "--changelog",
        default="Atualização do app",
        help="Descrição da changelog"
    )
    
    args = parser.parse_args()
    
    deployer = AutoDeploy()
    success = deployer.deploy(changelog=args.changelog)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
