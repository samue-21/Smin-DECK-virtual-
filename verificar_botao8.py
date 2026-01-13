#!/usr/bin/env python3
"""
Verificar arquivo do botao 8
"""

import os
import json
from pathlib import Path

DECK_FILE = './deck_config.sdk'

def inspecionar_botao8():
    """Verificar arquivo do botao 8"""
    print("="*80)
    print("[INSPECAO] Botao 8 - Arquivo e configuracao")
    print("="*80)
    
    if os.path.exists(DECK_FILE):
        print(f"\n📁 Arquivo config: {DECK_FILE}")
        with open(DECK_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Botao 8 (indice 7 ou 8)
        for idx in [7, 8]:
            if str(idx) in config:
                botao_config = config[str(idx)]
                print(f"\n[BOTAO {idx}]")
                print(json.dumps(botao_config, indent=2, ensure_ascii=False))
                
                file_path = botao_config.get('file')
                if file_path:
                    print(f"\n📄 Arquivo: {file_path}")
                    print(f"   Existe: {os.path.exists(file_path)}")
                    
                    if os.path.exists(file_path):
                        tamanho = os.path.getsize(file_path)
                        ext = Path(file_path).suffix.lower()
                        print(f"   Extensao: {ext}")
                        print(f"   Tamanho: {tamanho} bytes")
                        
                        # Se for .bin, mostrar magic bytes
                        if ext == '.bin':
                            with open(file_path, 'rb') as f:
                                magic = f.read(32)
                                print(f"   Magic bytes: {magic[:16].hex()}")
                                
                                # Tentar detectar tipo
                                if magic[4:8] == b'ftyp':
                                    print(f"   ⚠️  Detectado: Provavelmente MP4")
                                elif magic[0:8] == b'\x89PNG\r\n\x1a\n':
                                    print(f"   ⚠️  Detectado: Provavelmente PNG")
                                elif magic[0:3] == b'\xFF\xD8\xFF':
                                    print(f"   ⚠️  Detectado: Provavelmente JPEG")
                        
                        print(f"\n   ✅ Arquivo existe e pode ser verificado")
                    else:
                        print(f"\n   ❌ ARQUIVO NAO ENCONTRADO!")
                else:
                    print(f"\n   ℹ️  Sem arquivo atribuido")
    else:
        print(f"\n❌ Arquivo nao encontrado: {DECK_FILE}")

if __name__ == '__main__':
    inspecionar_botao8()
