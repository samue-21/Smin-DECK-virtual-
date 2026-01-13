"""
Deploy script para Smin-DECK Virtual
Empacota e faz upload das atualizações para o VPS
"""

import os
import json
import zipfile
import requests
from pathlib import Path
from datetime import datetime


class Deployer:
    def __init__(self):
        self.vps_url = "http://72.60.244.240:8000"
        self.deploy_endpoint = f"{self.vps_url}/api/deploy"
        self.version_file = "version.json"
        
    def get_current_version(self):
        """Lê versão atual"""
        try:
            with open(self.version_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('version', '0.0.0')
        except:
            return "0.0.0"
    
    def create_update_package(self):
        """Cria pacote ZIP com arquivos atualizáveis"""
        version = self.get_current_version()
        zip_name = f"smin_deck_v{version}.zip"
        
        print(f"📦 Criando pacote de atualização v{version}...")
        
        files_to_include = [
            "deck_window.py",
            "bot.py",
            "auto_updater.py",
            "theme.py",
            "bot_connector.py",
            "version.json",
            "requirements.txt"
        ]
        
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files_to_include:
                if os.path.exists(file):
                    zipf.write(file, arcname=file)
                    print(f"  ✅ {file}")
        
        size_mb = os.path.getsize(zip_name) / (1024 * 1024)
        print(f"✅ Pacote criado: {zip_name} ({size_mb:.2f} MB)")
        
        return zip_name
    
    def upload_to_vps(self, zip_file, changelog="Atualizações gerais"):
        """Faz upload do pacote para o VPS"""
        try:
            version = self.get_current_version()
            
            print(f"\n📤 Fazendo upload para VPS...")
            
            with open(zip_file, 'rb') as f:
                files = {
                    'package': f,
                    'version': (None, version),
                    'changelog': (None, changelog),
                    'timestamp': (None, datetime.now().isoformat())
                }
                
                response = requests.post(
                    f"{self.deploy_endpoint}/upload",
                    files=files,
                    timeout=120
                )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Upload concluído!")
                print(f"   URL: {data.get('download_url', 'N/A')}")
                return True
            else:
                print(f"❌ Erro no upload: {response.status_code}")
                print(f"   Resposta: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao fazer upload: {e}")
            return False
    
    def publish_update(self, changelog="Atualizações gerais"):
        """Publica atualização: cria pacote e faz upload"""
        print("🚀 Iniciando deployment...")
        print(f"Versão: {self.get_current_version()}")
        
        zip_file = self.create_update_package()
        success = self.upload_to_vps(zip_file, changelog)
        
        if success:
            # Limpar ZIP local
            try:
                os.remove(zip_file)
                print(f"🗑️ Arquivo local removido")
            except:
                pass
            
            print("\n✅ Deployment concluído com sucesso!")
            print("💡 Os clientes baixarão a atualização na próxima sincronização")
        else:
            print("\n❌ Deployment falhou!")
        
        return success


def main():
    import sys
    
    deployer = Deployer()
    
    # Changelog opcional por CLI
    changelog = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Atualizações gerais"
    
    deployer.publish_update(changelog)


if __name__ == "__main__":
    main()
