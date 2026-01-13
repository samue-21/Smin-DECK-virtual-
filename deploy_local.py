"""
Deploy Local - Simula servidor de updates localmente para testes
Útil enquanto o VPS não está disponível
"""

import os
import json
import zipfile
from pathlib import Path
from datetime import datetime


class LocalDeployer:
    def __init__(self):
        self.updates_dir = "updates_local"
        os.makedirs(self.updates_dir, exist_ok=True)
        self.version_file = os.path.join(self.updates_dir, "current_version.json")
        
    def get_current_version(self):
        """Lê versão atual"""
        try:
            with open("version.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('version', '0.0.0')
        except:
            return "0.0.0"
    
    def create_update_package(self):
        """Cria pacote ZIP com arquivos atualizáveis"""
        version = self.get_current_version()
        zip_name = os.path.join(self.updates_dir, f"smin_deck_v{version}.zip")
        
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
        
        return zip_name, version
    
    def publish_update_locally(self, changelog="Atualizações gerais"):
        """Publica atualização localmente"""
        print("🚀 Publicando atualização localmente...")
        print(f"Versão: {self.get_current_version()}")
        
        zip_file, version = self.create_update_package()
        
        # Atualizar versão no repositório local
        download_url = f"file://{os.path.abspath(zip_file)}"
        
        version_data = {
            "version": version,
            "download_url": download_url,
            "changelog": changelog,
            "released": datetime.now().isoformat(),
            "file_size": os.path.getsize(zip_file),
            "local": True
        }
        
        with open(self.version_file, 'w') as f:
            json.dump(version_data, f, indent=2)
        
        print(f"\n✅ Atualização publicada localmente!")
        print(f"   Arquivo: {zip_file}")
        print(f"   URL: {download_url}")
        print(f"   Versão: {version}")
        
        return True


def main():
    import sys
    
    deployer = LocalDeployer()
    changelog = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Atualizações gerais"
    
    deployer.publish_update_locally(changelog)


if __name__ == "__main__":
    main()
