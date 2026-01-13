#!/usr/bin/env python3
"""
Limpar fila de atualizacoes na API
"""

import requests

API_URL = "http://72.60.244.240:5001"

def listar():
    """Listar atualizacoes"""
    try:
        resp = requests.get(f'{API_URL}/api/atualizacoes', timeout=10)
        if resp.status_code == 200:
            return resp.json().get('atualizacoes', [])
    except Exception as e:
        print(f"[ERRO] Nao conseguiu listar: {e}")
    return []

def deletar_uma(att_id):
    """Deletar uma atualizacao"""
    print(f"\n[TESTE] Tentando deletar ID={att_id}...")
    print(f"  URL: DELETE {API_URL}/api/atualizacao/{att_id}")
    
    try:
        resp = requests.delete(f'{API_URL}/api/atualizacao/{att_id}', timeout=10)
        print(f"  Status: {resp.status_code}")
        print(f"  Response: {resp.text[:100]}")
        
        if resp.status_code == 200:
            print(f"  ✅ SUCESSO - Deletada!")
            return True
        else:
            print(f"  ❌ FALHA - Nao foi deletada")
            return False
    except Exception as e:
        print(f"  ❌ ERRO: {e}")
        return False

def main():
    atualizacoes = listar()
    
    if not atualizacoes:
        print("Fila vazia")
        return
    
    print(f"Total: {len(atualizacoes)} atualizacoes\n")
    
    # Tentar deletar a primeira
    primeira = atualizacoes[0]
    att_id = primeira['id']
    
    sucesso = deletar_uma(att_id)
    
    if sucesso:
        print("\n" + "="*80)
        resposta = input(f"✅ Deletar sucesso! Deseja limpar TODAS as {len(atualizacoes)} atualizacoes? (s/n): ").strip().lower()
        
        if resposta == 's':
            deletadas = 0
            for att in atualizacoes:
                try:
                    resp = requests.delete(f'{API_URL}/api/atualizacao/{att["id"]}', timeout=10)
                    if resp.status_code == 200:
                        print(f"  ✅ ID={att['id']}")
                        deletadas += 1
                except:
                    pass
            
            print(f"\n✅ {deletadas} deletadas com sucesso!")
            
            # Verificar
            atualizacoes_restantes = listar()
            print(f"Fila agora tem: {len(atualizacoes_restantes)} atualizacoes")
    else:
        print("\n" + "="*80)
        print("❌ Nao conseguiu deletar")
        print("\nPossíveis motivos:")
        print("1. Endpoint /api/atualizacao/<id> nao existe no servidor")
        print("2. Servidor retorna erro de autenticacao")
        print("3. Conectividade com VPS com problema")
        print("\nVerifique o api_server.py no VPS")

if __name__ == '__main__':
    main()
