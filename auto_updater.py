"""
Auto-Updater para Smin-DECK Virtual
Sincroniza automaticamente com múltiplos servidores para baixar atualizações
"""

import os
import json
import shutil
import requests
import subprocess
import sys
import time
from pathlib import Path
from update_config import get_active_endpoints


class AutoUpdater:
    def __init__(self):
        self.active_endpoints = get_active_endpoints()
        self.version_file = "version.json"
        self.current_version = self.get_local_version()
        self.app_path = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent
        
    def get_local_version(self):
        """Lê versão local do arquivo version.json"""
        try:
            if os.path.exists(self.version_file):
                with open(self.version_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('version', '0.0.0')
        except Exception as e:
            print(f"❌ Erro ao ler versão local: {e}")
        return "0.0.0"
    
    def check_for_updates(self):
        """Verifica se há nova versão em qualquer endpoint ativo"""
        for endpoint_name, endpoint_config in self.active_endpoints:
            try:
                print(f"🔍 Verificando em {endpoint_config['name']}...", end=" ")
                
                url = endpoint_config['api_url'] + endpoint_config['check_endpoint']
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    remote_version = data.get('version', '0.0.0')
                    
                    if self._compare_versions(remote_version, self.current_version) > 0:
                        print(f"✅ Nova versão: {remote_version}")
                        return {
                            'has_update': True,
                            'version': remote_version,
                            'download_url': data.get('download_url'),
                            'changelog': data.get('changelog', ''),
                            'endpoint': endpoint_name
                        }
                    else:
                        print(f"⏭️ Já atualizado ({self.current_version})")
            except Exception as e:
                print(f"⚠️ Indisponível ({str(e)[:30]}...)")
        
        return {'has_update': False}
    
    def download_update(self, download_url):
        """Baixa os arquivos de atualização"""
        try:
            print(f"📥 Baixando atualização de {download_url}...")
            response = requests.get(download_url, timeout=60, stream=True)
            
            if response.status_code == 200:
                update_file = "smin_deck_update.zip"
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(update_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024*1024):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            progress = (downloaded / total_size * 100) if total_size > 0 else 0
                            print(f"Progress: {progress:.1f}%", end='\r')
                
                print(f"\n✅ Download concluído!")
                return update_file
        except Exception as e:
            print(f"❌ Erro ao baixar atualização: {e}")
        
        return None
    
    def extract_update(self, zip_file):
        """Extrai os arquivos de atualização"""
        try:
            import zipfile
            
            extract_dir = "update_temp"
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            print(f"✅ Arquivos extraídos em {extract_dir}")
            return extract_dir
        except Exception as e:
            print(f"❌ Erro ao extrair atualização: {e}")
        
        return None
    
    def apply_update(self, extract_dir):
        """Copia arquivos atualizados para o local correto"""
        try:
            # Copiar arquivos Python principais
            for py_file in Path(extract_dir).glob("*.py"):
                if py_file.name not in ["auto_updater.py", "main.py"]:
                    shutil.copy2(py_file, py_file.name)
                    print(f"✅ Atualizado: {py_file.name}")
            
            # Atualizar versão
            if os.path.exists(os.path.join(extract_dir, "version.json")):
                shutil.copy2(os.path.join(extract_dir, "version.json"), self.version_file)
                self.current_version = self.get_local_version()
                print(f"✅ Versão agora: {self.current_version}")
            
            # Limpar
            shutil.rmtree(extract_dir, ignore_errors=True)
            return True
        except Exception as e:
            print(f"❌ Erro ao aplicar atualização: {e}")
        
        return False
    
    def _compare_versions(self, v1, v2):
        """Compara versões: retorna 1 se v1 > v2, -1 se v1 < v2, 0 se igual"""
        try:
            v1_parts = [int(x) for x in v1.split('.')]
            v2_parts = [int(x) for x in v2.split('.')]
            
            for i in range(max(len(v1_parts), len(v2_parts))):
                p1 = v1_parts[i] if i < len(v1_parts) else 0
                p2 = v2_parts[i] if i < len(v2_parts) else 0
                
                if p1 > p2:
                    return 1
                elif p1 < p2:
                    return -1
            
            return 0
        except:
            return 0
    
    def run_update_cycle(self):
        """Executa ciclo completo de atualização"""
        update_info = self.check_for_updates()
        
        if update_info['has_update']:
            print(f"\n🔄 Atualizando para v{update_info['version']}...")
            print(f"Changelog: {update_info['changelog']}")
            
            zip_file = self.download_update(update_info['download_url'])
            if zip_file:
                extract_dir = self.extract_update(zip_file)
                if extract_dir:
                    if self.apply_update(extract_dir):
                        print("✅ Atualização aplicada com sucesso!")
                        os.remove(zip_file)
                        return True
        
        return False


def start_auto_update_daemon(interval=60):
    """Inicia daemon de atualização em background (a cada 1 minuto por padrão para testes, depois 3600s para produção)"""
    updater = AutoUpdater()
    
    print("🚀 Daemon de atualização iniciado")
    print(f"Versão atual: {updater.current_version}")
    print(f"Endpoints ativos: {len(updater.active_endpoints)}")
    print(f"Intervalo de verificação: {interval}s")
    
    while True:
        try:
            updater.run_update_cycle()
        except Exception as e:
            print(f"⚠️ Erro no ciclo de atualização: {e}")
        
        time.sleep(interval)


if __name__ == "__main__":
    # Teste rápido
    updater = AutoUpdater()
    print(f"Versão local: {updater.current_version}")
    print(f"Endpoints ativos: {len(updater.active_endpoints)}")
    
    update_info = updater.check_for_updates()
    print(f"Update disponível: {update_info.get('has_update', False)}")
    
    def download_update(self, download_url):
        """Baixa os arquivos de atualização do VPS"""
        try:
            print(f"📥 Baixando atualização de {download_url}...")
            response = requests.get(download_url, timeout=60, stream=True)
            
            if response.status_code == 200:
                update_file = "smin_deck_update.zip"
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(update_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024*1024):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            progress = (downloaded / total_size * 100) if total_size > 0 else 0
                            print(f"Progress: {progress:.1f}%", end='\r')
                
                print(f"\n✅ Download concluído!")
                return update_file
        except Exception as e:
            print(f"❌ Erro ao baixar atualização: {e}")
        
        return None
    
    def extract_update(self, zip_file):
        """Extrai os arquivos de atualização"""
        try:
            import zipfile
            
            extract_dir = "update_temp"
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            print(f"✅ Arquivos extraídos em {extract_dir}")
            return extract_dir
        except Exception as e:
            print(f"❌ Erro ao extrair atualização: {e}")
        
        return None
    
    def apply_update(self, extract_dir):
        """Copia arquivos atualizados para o local correto"""
        try:
            # Copiar arquivos Python principais
            for py_file in Path(extract_dir).glob("*.py"):
                if py_file.name not in ["auto_updater.py", "main.py"]:
                    shutil.copy2(py_file, py_file.name)
                    print(f"✅ Atualizado: {py_file.name}")
            
            # Atualizar versão
            if os.path.exists(os.path.join(extract_dir, "version.json")):
                shutil.copy2(os.path.join(extract_dir, "version.json"), self.version_file)
                self.current_version = self.get_local_version()
                print(f"✅ Versão agora: {self.current_version}")
            
            # Limpar
            shutil.rmtree(extract_dir, ignore_errors=True)
            return True
        except Exception as e:
            print(f"❌ Erro ao aplicar atualização: {e}")
        
        return False
    
    def _compare_versions(self, v1, v2):
        """Compara versões: retorna 1 se v1 > v2, -1 se v1 < v2, 0 se igual"""
        try:
            v1_parts = [int(x) for x in v1.split('.')]
            v2_parts = [int(x) for x in v2.split('.')]
            
            for i in range(max(len(v1_parts), len(v2_parts))):
                p1 = v1_parts[i] if i < len(v1_parts) else 0
                p2 = v2_parts[i] if i < len(v2_parts) else 0
                
                if p1 > p2:
                    return 1
                elif p1 < p2:
                    return -1
            
            return 0
        except:
            return 0
    
    def run_update_cycle(self):
        """Executa ciclo completo de atualização"""
        update_info = self.check_for_updates()
        
        if update_info['has_update']:
            print(f"\n🔄 Atualizando para v{update_info['version']}...")
            print(f"Changelog: {update_info['changelog']}")
            
            zip_file = self.download_update(update_info['download_url'])
            if zip_file:
                extract_dir = self.extract_update(zip_file)
                if extract_dir:
                    if self.apply_update(extract_dir):
                        print("✅ Atualização aplicada com sucesso!")
                        os.remove(zip_file)
                        return True
        
        return False


def start_auto_update_daemon(interval=60):
    """Inicia daemon de atualização em background (a cada 1 minuto por padrão para testes, depois 3600s para produção)"""
    updater = AutoUpdater()
    
    print("🚀 Daemon de atualização iniciado")
    print(f"Versão atual: {updater.current_version}")
    print(f"Intervalo de verificação: {interval}s")
    
    while True:
        try:
            updater.run_update_cycle()
        except Exception as e:
            print(f"⚠️ Erro no ciclo de atualização: {e}")
        
        time.sleep(interval)


if __name__ == "__main__":
    # Teste rápido
    updater = AutoUpdater()
    print(f"Versão local: {updater.current_version}")
    
    update_info = updater.check_for_updates()
    print(f"Update disponível: {update_info.get('has_update', False)}")
