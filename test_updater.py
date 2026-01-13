#!/usr/bin/env python3
"""
Script de teste do auto-updater
"""

import requests
import json

# Testar endpoint do VPS
print("🧪 Testando auto-updater...")
print("=" * 60)

# 1. Verificar versão local
print("\n1️⃣ Versão local:")
try:
    with open("version.json", "r", encoding="utf-8") as f:
        local_version = json.load(f)
        print(f"   Versão: {local_version.get('version')}")
        print(f"   Build: {local_version.get('build')}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 2. Verificar endpoint VPS
print("\n2️⃣ Verificando endpoint VPS (72.60.244.240:8001)...")
try:
    url = "http://72.60.244.240:8000/api/updates/check"
    print(f"   URL: {url}")
    response = requests.get(url, timeout=5)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        remote_version = response.json()
        print(f"   Versão no servidor: {remote_version.get('version')}")
        print(f"   Download URL: {remote_version.get('download_url')}")
        print(f"   Changelog: {remote_version.get('changelog', 'N/A')}")
    else:
        print(f"   ❌ Status não é 200: {response.text[:100]}")
except requests.exceptions.Timeout:
    print(f"   ❌ Timeout - Servidor não respondeu")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 3. Testar comparação de versão
print("\n3️⃣ Teste de comparação de versão:")

def compare_versions(v1, v2):
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

# Testes
tests = [
    ("1.0.1", "1.0.0", 1, "1.0.1 > 1.0.0"),
    ("1.0.0", "1.0.1", -1, "1.0.0 < 1.0.1"),
    ("1.0.0", "1.0.0", 0, "1.0.0 = 1.0.0"),
    ("2.0.0", "1.9.9", 1, "2.0.0 > 1.9.9"),
]

for v1, v2, expected, desc in tests:
    result = compare_versions(v1, v2)
    status = "✅" if result == expected else "❌"
    print(f"   {status} {desc} (resultado: {result})")

print("\n" + "=" * 60)
print("✅ Teste concluído")
