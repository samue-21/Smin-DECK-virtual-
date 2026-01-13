#!/usr/bin/env python3
"""
Converter arquivos .bin para extensao real
Detecta tipo pelos magic bytes e renomeia
"""

import os
from pathlib import Path

DOWNLOADS_DIR = os.path.expanduser('~/.smindeckbot/downloads')

def detect_bin_extension(file_path: str) -> str:
    """Detecta extensao real de arquivo .bin"""
    try:
        with open(file_path, 'rb') as f:
            magic_bytes = f.read(32)
        
        # ZIP
        if magic_bytes[0:4] == b'PK\x03\x04':
            return '.zip'
        # MP4
        elif magic_bytes[4:8] == b'ftyp':
            return '.mp4'
        # MKV
        elif magic_bytes[0:4] == b'\x1A\x45\xDF\xA3':
            return '.mkv'
        # PNG
        elif magic_bytes[0:8] == b'\x89PNG\r\n\x1a\n':
            return '.png'
        # JPEG
        elif magic_bytes[0:3] == b'\xFF\xD8\xFF':
            return '.jpg'
        # GIF
        elif magic_bytes[0:6] in (b'GIF87a', b'GIF89a'):
            return '.gif'
        # BMP
        elif magic_bytes[0:2] == b'BM':
            return '.bmp'
        # WebP
        elif magic_bytes[0:4] == b'RIFF' and magic_bytes[8:12] == b'WEBP':
            return '.webp'
        # MP3
        elif magic_bytes[0:3] == b'ID3' or magic_bytes[0:2] == b'\xFF\xFB':
            return '.mp3'
        # WAV
        elif magic_bytes[0:4] == b'RIFF' and magic_bytes[8:12] == b'WAVE':
            return '.wav'
        # OGG
        elif magic_bytes[0:4] == b'OggS':
            return '.ogg'
    except:
        pass
    
    return '.bin'

def converter_bins():
    """Converter todos os .bin para extensao real"""
    print("="*80)
    print("[CONVERSAO] Detectando e renomeando arquivos .bin")
    print("="*80)
    
    if not os.path.exists(DOWNLOADS_DIR):
        print(f"\n❌ Diretorio nao existe: {DOWNLOADS_DIR}")
        return
    
    arquivos = os.listdir(DOWNLOADS_DIR)
    bins = [a for a in arquivos if a.endswith('.bin')]
    
    if not bins:
        print(f"\n✅ Nenhum arquivo .bin encontrado")
        return
    
    print(f"\n📋 Encontrados {len(bins)} arquivos .bin:\n")
    
    for bin_file in bins:
        bin_path = os.path.join(DOWNLOADS_DIR, bin_file)
        ext_real = detect_bin_extension(bin_path)
        
        if ext_real == '.bin':
            print(f"  ⚠️  {bin_file:40} → Tipo desconhecido (mantendo .bin)")
        else:
            # Criar novo nome
            stem = Path(bin_file).stem
            new_filename = f"{stem}{ext_real}"
            new_path = os.path.join(DOWNLOADS_DIR, new_filename)
            
            try:
                os.rename(bin_path, new_path)
                print(f"  ✅ {bin_file:40} → {new_filename}")
            except Exception as e:
                print(f"  ❌ {bin_file:40} → ERRO: {e}")

if __name__ == '__main__':
    converter_bins()
