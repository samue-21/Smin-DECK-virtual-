#!/usr/bin/env python3
"""
Monitor do auto-updater
Aguarda e verifica se o auto-update foi executado
"""

import time
import json
import os
from pathlib import Path

print("🔍 Monitorando auto-updater...")
print("=" * 60)
print("Aguardando daemon executar (próximos 90 segundos)...")
print("=" * 60)

installed_path = Path("C:/Program Files/SminDeck")
version_file = installed_path / "version.json"

initial_version = None
if version_file.exists():
    with open(version_file, 'r') as f:
        data = json.load(f)
        initial_version = data.get('version')
        print(f"\n📌 Versão inicial: {initial_version}")
else:
    print(f"\n⚠️  version.json não encontrado em {installed_path}")

print("\n⏳ Monitorando...")

for i in range(90):
    time.sleep(1)
    
    if i % 10 == 0 and i > 0:
        print(f"  {i}s...")
    
    if version_file.exists():
        try:
            with open(version_file, 'r') as f:
                data = json.load(f)
                current_version = data.get('version')
                
                if current_version and current_version != initial_version:
                    print(f"\n✅ ATUALIZAÇÃO DETECTADA!")
                    print(f"   Versão anterior: {initial_version}")
                    print(f"   Versão atual: {current_version}")
                    print(f"   Build: {data.get('build')}")
                    break
        except:
            pass

print("\n" + "=" * 60)
print("Monitoramento concluído")
