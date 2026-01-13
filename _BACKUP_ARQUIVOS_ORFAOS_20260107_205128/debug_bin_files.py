#!/usr/bin/env python3
"""
Script para debugar arquivos .bin salvos
"""
import os
import glob

downloads_dir = os.path.expanduser("~/.smindeckbot/downloads/")

print(f"📂 Procurando por arquivos .bin em {downloads_dir}")

if not os.path.exists(downloads_dir):
    print("❌ Diretório não existe")
else:
    bin_files = glob.glob(os.path.join(downloads_dir, "*.bin"))
    
    if not bin_files:
        print("❌ Nenhum arquivo .bin encontrado")
    else:
        for bin_file in bin_files:
            print(f"\n📄 {os.path.basename(bin_file)}")
            print(f"   Tamanho: {os.path.getsize(bin_file)} bytes")
            
            with open(bin_file, 'rb') as f:
                magic = f.read(32)
            
            print(f"   Magic bytes (hex): {magic.hex()[:64]}")
            print(f"   Magic bytes (ascii): {repr(magic[:16])}")
            
            # Tentar detectar tipo
            if magic[4:8] == b'ftyp':
                print(f"   ✅ DETECTADO: MP4")
            elif magic[0:8] == b'\x89PNG\r\n\x1a\n':
                print(f"   ✅ DETECTADO: PNG")
            elif magic[0:3] == b'\xFF\xD8\xFF':
                print(f"   ✅ DETECTADO: JPEG")
            elif magic[0:6] in (b'GIF87a', b'GIF89a'):
                print(f"   ✅ DETECTADO: GIF")
            elif magic[0:4] == b'RIFF' and magic[8:12] == b'WEBP':
                print(f"   ✅ DETECTADO: WebP")
            elif magic[0:4] == b'RIFF' and magic[8:12] == b'WAVE':
                print(f"   ✅ DETECTADO: WAV")
            elif magic[0:4] == b'OggS':
                print(f"   ✅ DETECTADO: OGG")
            elif magic[0:3] == b'ID3' or magic[0:2] == b'\xFF\xFB':
                print(f"   ✅ DETECTADO: MP3")
            elif magic[0:2] == b'BM':
                print(f"   ✅ DETECTADO: BMP")
            elif magic.startswith(b'<!DOCTYPE') or magic.startswith(b'<html'):
                print(f"   ❌ DETECTADO: HTML (ERRO - arquivo corrompido)")
            else:
                print(f"   ❓ TIPO DESCONHECIDO")
    
    # Também mostrar todos os arquivos no diretório
    print("\n" + "="*60)
    print("📋 Todos os arquivos no diretório:")
    for file in os.listdir(downloads_dir):
        filepath = os.path.join(downloads_dir, file)
        size = os.path.getsize(filepath)
        print(f"   {file} ({size} bytes)")
