#!/usr/bin/env python3
"""
Script para limpar atualizacoes OLD/duplicadas da fila da API
Remove atualizacoes que estao ha muito tempo sem mudar
"""

import requests
import json
from datetime import datetime, timedelta

API_URL = "http://72.60.244.240:5001"

def listar_atualizacoes():
    """Listar todas as atualizacoes da API"""
    try:
        resp = requests.get(f'{API_URL}/api/atualizacoes', timeout=10)
        if resp.status_code == 200:
            return resp.json().get('atualizacoes', [])
    except Exception as e:
        print(f"[ERRO] Nao conseguiu conectar na API: {e}")
    return []

def deletar_atualizacao(atualizacao_id):
    """Deletar uma atualizacao da fila"""
    try:
        resp = requests.delete(f'{API_URL}/api/atualizacoes/{atualizacao_id}', timeout=10)
        if resp.status_code == 200:
            return True
    except Exception:
        pass
    return False

def main():
    print("="*80)
    print("[LIMPEZA] Inspecionando fila de atualizacoes da API")
    print("="*80)
    
    atualizacoes = listar_atualizacoes()
    
    if not atualizacoes:
        print("\n✅ Fila vazia")
        return
    
    print(f"\n📋 Total: {len(atualizacoes)} atualizacoes\n")
    
    # Listar todas
    for idx, att in enumerate(atualizacoes, 1):
        print(f"[{idx}] ID={att.get('id')} | Bot={att.get('botao')} | Tipo={att.get('tipo')}")
        print(f"    Dados: {json.dumps(att.get('dados', {}), ensure_ascii=False)[:60]}...")
        print(f"    Criada em: {att.get('criada_em', 'N/A')}\n")
    
    # Perguntar se quer limpar
    print("="*80)
    resposta = input("🗑️  Deseja LIMPAR TODA A FILA? (s/n): ").strip().lower()
    
    if resposta == 's':
        deletadas = 0
        for att in atualizacoes:
            att_id = att.get('id')
            if deletar_atualizacao(att_id):
                print(f"  ✅ ID={att_id} deletada")
                deletadas += 1
            else:
                print(f"  ❌ Erro ao deletar ID={att_id}")
        
        print(f"\n✅ {deletadas}/{len(atualizacoes)} atualizacoes removidas da fila")
    else:
        print("\n⏭️  Operacao cancelada")

if __name__ == '__main__':
    main()
