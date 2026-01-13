#!/usr/bin/env python3
"""
Diagnosticar problema: 
- Arquivo ZIP está sendo deletado?
- App recebendo apenas nome vs conteúdo?
"""

import os
import requests
from pathlib import Path

API_URL = "http://72.60.244.240:5001"
DOWNLOADS_DIR = os.path.expanduser('~/.smindeckbot/downloads')

def testar_download_arquivo():
    """Testar download de um arquivo"""
    print("="*80)
    print("[TESTE] Download de arquivo da API")
    print("="*80)
    
    # Tentar baixar o video_botao_7.bin que está na API
    filename = "video_botao_7.bin"
    
    print(f"\n1. Tentando baixar: {filename}")
    print(f"   URL: {API_URL}/api/arquivo/{filename}")
    
    try:
        resp = requests.get(f'{API_URL}/api/arquivo/{filename}', timeout=30)
        print(f"\n2. Status: {resp.status_code}")
        print(f"   Content-Length (headers): {resp.headers.get('content-length', 'N/A')}")
        print(f"   Content Size (real): {len(resp.content)} bytes")
        print(f"   Content Type: {resp.headers.get('content-type', 'N/A')}")
        
        if resp.status_code == 200:
            # Verificar os primeiros bytes
            print(f"\n3. Primeiros bytes (magic): {resp.content[:4].hex()}")
            
            if resp.content[:2] == b'PK':
                print("   ✅ É um arquivo ZIP (magic bytes: 504b)")
            elif resp.content[:4] == bytes([0x00, 0x00, 0x00, 0x20]):
                print("   ✅ É um arquivo MP4")
            else:
                print(f"   ⚠️  Tipo desconhecido")
            
            print(f"\n4. Simulando save local...")
            test_path = os.path.join(DOWNLOADS_DIR, f"TEST_{filename}")
            with open(test_path, 'wb') as f:
                f.write(resp.content)
            
            print(f"   Salvo em: {test_path}")
            print(f"   Tamanho: {os.path.getsize(test_path)} bytes")
            print(f"   Existe: {os.path.exists(test_path)}")
            
            # Limpar teste
            try:
                os.remove(test_path)
                print(f"   Deletado: {test_path}")
            except:
                pass
        else:
            print(f"\n❌ Erro: {resp.status_code}")
            print(f"   Response: {resp.text[:200]}")
            
    except Exception as e:
        print(f"\n❌ ERRO: {e}")

def verificar_delecoes_automaticas():
    """Verificar se há script de limpeza automática rodando"""
    print("\n" + "="*80)
    print("[DIAGNOSTICO] Limpeza automática")
    print("="*80)
    
    print("\nArquivos que deletam automaticamente:")
    print("1. sincronizador.py - extrair_arquivo_compactado_cliente()")
    print("   └─ Deleta ZIP após extrair (correto)")
    print("   └─ ANTES: Copia arquivo extraído")
    
    print("\n2. sincronizador.py - baixar_arquivo()")
    print("   └─ Não deleta nada (correto)")
    
    print("\n3. limpar_atualizacoes_falhadas.py")
    print("   └─ Deleta arquivo FALHADO (após 2 tentativas)")
    print("   └─ Não deve afetar sucesso")
    
    print("\n⚠️  POSSÍVEL PROBLEMA:")
    print("   Se arquivo é deletado ANTES de extrair, arquivo fica perdido!")

if __name__ == '__main__':
    testar_download_arquivo()
    verificar_delecoes_automaticas()
