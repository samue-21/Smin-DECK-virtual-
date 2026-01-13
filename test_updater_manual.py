#!/usr/bin/env python3
"""
Teste manual do auto-updater
"""

import sys
import os

# Adicionar diretório ao path
sys.path.insert(0, os.getcwd())

from auto_updater import AutoUpdater

print("🧪 Testando auto-updater manualmente...")
print("=" * 60)

updater = AutoUpdater()

print(f"📌 Versão local: {updater.current_version}")
print(f"📌 Endpoints ativos: {len(updater.active_endpoints)}")

for name, config in updater.active_endpoints:
    print(f"   - {config['name']}: {config['api_url']}")

print("\n🔍 Verificando atualizações...")
update_info = updater.check_for_updates()

print(f"\nResultado:")
print(f"  Has update: {update_info.get('has_update')}")
print(f"  Version: {update_info.get('version')}")
print(f"  Download URL: {update_info.get('download_url')}")
print(f"  Changelog: {update_info.get('changelog')}")

if update_info.get('has_update'):
    print("\n💾 Tentando fazer download...")
    zip_file = updater.download_update(update_info['download_url'])
    if zip_file:
        print(f"   ✅ Download concluído: {zip_file}")
        
        print("\n📦 Tentando extrair...")
        extract_dir = updater.extract_update(zip_file)
        if extract_dir:
            print(f"   ✅ Extraído em: {extract_dir}")
            
            print("\n⚙️ Aplicando atualização...")
            if updater.apply_update(extract_dir):
                print(f"   ✅ Atualização aplicada!")
                print(f"   Nova versão: {updater.current_version}")
            else:
                print(f"   ❌ Erro ao aplicar")
        else:
            print(f"   ❌ Erro ao extrair")
    else:
        print(f"   ❌ Erro no download")
else:
    print("Nenhuma atualização disponível ou já está atualizado")

print("\n" + "=" * 60)
