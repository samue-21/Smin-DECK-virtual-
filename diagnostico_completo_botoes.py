#!/usr/bin/env python3
"""
Verificar arquivos e atualizacoes para todos os botoes
"""

import requests
import json
import os
from pathlib import Path

API_URL = "http://72.60.244.240:5001"
DECK_FILE = './deck_config.sdk'
DOWNLOADS_DIR = os.path.expanduser('~/.smindeckbot/downloads')

def main():
    print("="*80)
    print("[DIAGNOSTICO] Status de todos os botoes")
    print("="*80)
    
    # 1. Verificar config local
    print("\n[CONFIG LOCAL]")
    if os.path.exists(DECK_FILE):
        with open(DECK_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        for idx in range(12):
            if str(idx) in config:
                file_path = config[str(idx)].get('file')
                if file_path:
                    exists = os.path.exists(file_path)
                    ext = Path(file_path).suffix.lower()
                    status = "✅" if exists else "❌"
                    print(f"  Bot {idx}: {ext:8} {status} {os.path.basename(file_path)[:40]}")
                else:
                    print(f"  Bot {idx}: [vazio]")
    
    # 2. Verificar arquivos no downloads
    print("\n[ARQUIVOS NO DOWNLOADS]")
    if os.path.exists(DOWNLOADS_DIR):
        arquivos = os.listdir(DOWNLOADS_DIR)
        for arq in sorted(arquivos):
            size = os.path.getsize(os.path.join(DOWNLOADS_DIR, arq))
            ext = Path(arq).suffix.lower()
            print(f"  {arq:40} ({ext:6}) {size:12} bytes")
    
    # 3. Verificar atualizacoes na API
    print("\n[ATUALIZACOES NA FILA]")
    try:
        resp = requests.get(f'{API_URL}/api/atualizacoes', timeout=10)
        if resp.status_code == 200:
            atualizacoes = resp.json().get('atualizacoes', [])
            if atualizacoes:
                print(f"  Total: {len(atualizacoes)}\n")
                for att in atualizacoes:
                    bot = att.get('botao')
                    tipo = att.get('tipo')
                    dados = att.get('dados', {})
                    arquivo = dados.get('arquivo', '?')
                    print(f"    Bot {bot}: {tipo:8} {arquivo[:40]}")
            else:
                print("  Nenhuma atualizacao pendente")
    except Exception as e:
        print(f"  Erro ao conectar API: {e}")
    
    # 4. Diagnostico especifico do botao 8
    print("\n[DIAGNOSTICO - BOTAO 8]")
    if str(8) in config:
        botao8 = config[str(8)]
        file_path = botao8.get('file')
        if file_path:
            print(f"  Arquivo: {file_path}")
            if os.path.exists(file_path):
                ext = Path(file_path).suffix.lower()
                print(f"  Existe: Sim ({ext})")
            else:
                print(f"  Existe: Nao ❌")
        else:
            print(f"  Arquivo: Vazio")
            print(f"  Status: Botao sem arquivo atribuido")

if __name__ == '__main__':
    main()
