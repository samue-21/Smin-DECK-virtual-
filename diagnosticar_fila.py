#!/usr/bin/env python3
"""
Diagnostico completo da fila de atualizacoes
- Mostra o que a API tem
- Mostra o que o banco local tem
- Identifica problemas
"""

import requests
import sqlite3
import os

API_URL = "http://72.60.244.240:5001"
DB_PATH = os.path.expanduser('~/.smindeckbot/smindeckbot.db')

def listar_atualizacoes_api():
    """Listar da API"""
    try:
        resp = requests.get(f'{API_URL}/api/atualizacoes', timeout=10)
        if resp.status_code == 200:
            return resp.json().get('atualizacoes', [])
    except Exception as e:
        print(f"[ERRO] API indisponivel: {e}")
    return []

def listar_atualizacoes_db():
    """Listar do banco local"""
    if not os.path.exists(DB_PATH):
        return []
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, chave, tipo, botao, dados, tentativas FROM atualizacoes")
        return cursor.fetchall()
    except:
        return []
    finally:
        conn.close()

def main():
    print("="*80)
    print("[DIAGNOSTICO] Estado da fila de atualizacoes")
    print("="*80)
    
    # API
    print("\n[API]")
    att_api = listar_atualizacoes_api()
    print(f"  Total na API: {len(att_api)}")
    
    if att_api:
        print("\n  Detalhes:")
        for idx, att in enumerate(att_api, 1):
            print(f"    [{idx}] ID={att.get('id')} Bot={att.get('botao')} Tipo={att.get('tipo')}")
    
    # BANCO LOCAL
    print("\n[BANCO LOCAL]")
    att_db = listar_atualizacoes_db()
    print(f"  Total no DB: {len(att_db)}")
    
    if att_db:
        print("\n  Detalhes:")
        for idx, (id_att, chave, tipo, botao, dados, tentativas) in enumerate(att_db, 1):
            print(f"    [{idx}] ID={id_att} Bot={botao} Tipo={tipo} Tentativas={tentativas}")
    
    # DIAGNOSTICO
    print("\n" + "="*80)
    print("[DIAGNOSTICO]")
    print("="*80)
    
    if len(att_api) == 0 and len(att_db) == 0:
        print("\n✅ Sistema limpo - sem atualizacoes na fila")
    
    elif len(att_api) > 0 and len(att_db) == 0:
        print(f"\n⚠️  PROBLEMA: API tem {len(att_api)} atualizacoes mas banco local vazio")
        print("   → Atualizacoes nao estao sendo salvas no banco local")
        print("   → Endpoint /api/atualizacoes pode estar retornando dados diretamente")
        print("   → Deletar da API nao resolve o problema se vir de um servico externo")
    
    elif len(att_api) == 0 and len(att_db) > 0:
        print(f"\n⚠️  PROBLEMA: Banco tem {len(att_db)} mas API vazia")
        print("   → Atualizacoes deletadas da API mas nao do banco local")
        print("   → Banco local precisa limpar")
    
    else:
        print(f"\n⚠️  MISMATCH: API={len(att_api)} vs DB={len(att_db)}")
        print("   → Sincronizacao incompleta")
    
    # SOLUCOES
    print("\n" + "="*80)
    print("[SOLUCOES SUGERIDAS]")
    print("="*80)
    
    if len(att_api) > 0:
        print("\n1. Tentar deletar uma atualizacao da API:")
        print(f"   curl -X DELETE http://localhost:8000/api/atualizacao/{att_api[0]['id']}")
    
    if len(att_db) > 0:
        print("\n2. Limpar banco local:")
        print("   python limpar_banco_local.py")

if __name__ == '__main__':
    main()
