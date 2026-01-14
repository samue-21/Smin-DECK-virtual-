#!/usr/bin/env python3
import requests
import json

API_URL = 'http://localhost:5001'

print("🔍 Testando API...\n")

try:
    resp = requests.get(f'{API_URL}/api/atualizacoes', timeout=5)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text[:500]}\n")
    
    if resp.status_code == 200:
        dados = resp.json()
        print(f"✅ API respondendo!")
        atualizacoes = dados.get('atualizacoes', [])
        print(f"Atualizações encontradas: {len(atualizacoes)}\n")
        
        for att in atualizacoes:
            print(f"  Botão {att['botao']}: {att['tipo']}")
            print(f"    Dados: {att['dados']}")
    else:
        print(f"❌ API retornou erro {resp.status_code}")
        
except Exception as e:
    print(f"❌ Erro ao conectar API: {e}")
    print(f"Tipo do erro: {type(e).__name__}")
