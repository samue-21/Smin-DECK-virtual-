#!/usr/bin/env python3
"""
Script de teste final: Verifica se a extração de .bin funciona corretamente
"""

import os
import json
from sincronizador import extrair_arquivo_compactado_cliente

print("=" * 70)
print("TESTE FINAL: EXTRAÇÃO DE ARQUIVO .BIN (ZIP)")
print("=" * 70)

# Testar com arquivo que existe
bin_file = os.path.expanduser('~/.smindeckbot/downloads/video_botao_6.bin')

if not os.path.exists(bin_file):
    print(f"❌ Arquivo não encontrado: {bin_file}")
    exit(1)

print(f"\n✓ Arquivo encontrado: {bin_file}")
print(f"  Tamanho: {os.path.getsize(bin_file):,} bytes")

# Testar extração
print(f"\n[TEST] Executando extrair_arquivo_compactado_cliente()...")
resultado = extrair_arquivo_compactado_cliente(bin_file, 'video')

print(f"\n[RESULTADO]:")
if resultado:
    print(f"  ✓ Caminho retornado: {resultado}")
    if os.path.exists(resultado):
        tamanho = os.path.getsize(resultado)
        print(f"  ✓ Arquivo existe")
        print(f"  ✓ Tamanho: {tamanho:,} bytes")
        
        if tamanho > 100000:  # Maior que 100KB
            print(f"  ✅ SUCESSO! Arquivo extraído corretamente.")
        else:
            print(f"  ❌ AVISO: Arquivo pequeno demais ({tamanho} bytes)")
    else:
        print(f"  ❌ Arquivo não existe!")
else:
    print(f"  ❌ Função retornou None")

# Verificar arquivos em downloads
print(f"\n[DOWNLOADS]:")
downloads_dir = os.path.expanduser('~/.smindeckbot/downloads')
if os.path.exists(downloads_dir):
    files = sorted(os.listdir(downloads_dir))
    for f in files:
        path = os.path.join(downloads_dir, f)
        size = os.path.getsize(path)
        print(f"  - {f}: {size:,} bytes")

print("\n" + "=" * 70)
