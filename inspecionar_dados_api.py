#!/usr/bin/env python3
"""
Inspecionar estrutura dos dados que a API retorna
"""

import requests
import json

API_URL = "http://72.60.244.240:5001"

def inspecionar():
    print("[INSPECAO] Estrutura de dados retornados pela API\n")
    
    try:
        resp = requests.get(f'{API_URL}/api/atualizacoes', timeout=10)
        if resp.status_code != 200:
            print(f"❌ Erro na API: {resp.status_code}")
            return
        
        dados = resp.json()
        print(f"JSON Response completo:\n{json.dumps(dados, indent=2, ensure_ascii=False)[:500]}...\n")
        
        atualizacoes = dados.get('atualizacoes', [])
        
        if not atualizacoes:
            print("⚠️  Nenhuma atualizacao retornada")
            return
        
        print(f"Total: {len(atualizacoes)} atualizacoes\n")
        
        # Inspecionar primeira
        att = atualizacoes[0]
        print("="*80)
        print("[PRIMEIRA ATUALIZACAO]")
        print("="*80)
        print(f"Type: {type(att)}")
        print(f"Keys: {att.keys() if hasattr(att, 'keys') else 'N/A'}")
        print(f"\nConteudo:\n{json.dumps(att, indent=2, ensure_ascii=False)}\n")
        
        # Verificar 'dados'
        print("="*80)
        print("[CAMPO 'dados']")
        print("="*80)
        dados_campo = att.get('dados')
        print(f"Type: {type(dados_campo)}")
        print(f"Value: {dados_campo}")
        print(f"Repr: {repr(dados_campo)}")
        
        # Tentar acessar como dict
        print("\nTentativas de acesso:")
        if isinstance(dados_campo, dict):
            print(f"  ✅ eh um dict")
            print(f"     'arquivo' in dados = {'arquivo' in dados_campo}")
            print(f"     'conteudo' in dados = {'conteudo' in dados_campo}")
        elif isinstance(dados_campo, str):
            print(f"  ⚠️  eh uma STRING")
            try:
                parsed = json.loads(dados_campo)
                print(f"     Pode fazer parse JSON: {type(parsed)}")
                print(f"     'arquivo' in parsed = {'arquivo' in parsed}")
            except:
                print(f"     NAO pode fazer parse JSON")
        else:
            print(f"  ❌ Tipo desconhecido")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    inspecionar()
