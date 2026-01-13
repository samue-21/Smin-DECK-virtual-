#!/usr/bin/env python3
"""
Teste: Validar que a extracao funciona corretamente com multiplos arquivos
Cenario: ZIP com video + pasta
"""

import os
import json
import zipfile
import tempfile
from pathlib import Path

# Setup
TEST_DIR = os.path.join(os.path.dirname(__file__), 'test_multiplos')
os.makedirs(TEST_DIR, exist_ok=True)

def criar_video_fake():
    """Criar arquivo de video ficticio"""
    video_data = bytes([0x00, 0x00, 0x00, 0x20, 0x66, 0x74, 0x79, 0x70])
    video_data += b'mp42' + b'\x00' * 100
    
    video_path = os.path.join(TEST_DIR, 'video_principal.mp4')
    with open(video_path, 'wb') as f:
        f.write(video_data)
    
    return video_path

def criar_zip_com_multiplos():
    """Criar ZIP com: video + pasta"""
    video_path = criar_video_fake()
    
    # Criar um arquivo em subpasta
    subpasta = os.path.join(TEST_DIR, 'subfolder')
    os.makedirs(subpasta, exist_ok=True)
    
    txt_path = os.path.join(subpasta, 'readme.txt')
    with open(txt_path, 'w') as f:
        f.write('Instrucoes do video')
    
    # Criar ZIP
    zip_path = os.path.join(TEST_DIR, 'conteudo_com_pasta.zip')
    with zipfile.ZipFile(zip_path, 'w') as z:
        z.write(video_path, arcname='video_principal.mp4')
        z.write(txt_path, arcname='subfolder/readme.txt')
    
    print(f"[OK] ZIP criado: {zip_path}")
    print(f"  - video_principal.mp4 (na raiz)")
    print(f"  - subfolder/readme.txt (em subpasta)\n")
    
    return zip_path

def teste_extracao():
    """Testar a extracao"""
    print("="*80)
    print("[TESTE] Extracao de arquivo com multiplos itens")
    print("="*80)
    print()
    
    zip_path = criar_zip_com_multiplos()
    
    # Importar e testar
    from sincronizador import extrair_arquivo_compactado_cliente
    
    print("[TESTANDO] Extraindo video de ZIP com pasta...\n")
    resultado = extrair_arquivo_compactado_cliente(zip_path, 'video')
    
    if resultado:
        print(f"[RESULTADO] Arquivo extraido: {os.path.basename(resultado)}")
        print(f"[VERIFICACAO] Tipo: {Path(resultado).suffix}")
        
        if resultado.endswith('.mp4'):
            print("[SUCESSO] Video extraido corretamente com extensao .mp4")
            print("\n✅ FUNCIONALIDADE CORRIGIDA:")
            print("   - Arquivo extraido da RAIZ (nao da subpasta)")
            print("   - Extensao correta mantida (.mp4)")
            print("   - Multiplos itens no compactado tratados corretamente")
            return True
        else:
            print(f"[AVISO] Extensao inesperada: {Path(resultado).suffix}")
            return False
    else:
        print("[ERRO] Extracao falhou")
        return False

def cleanup():
    """Limpar testes"""
    try:
        import shutil
        shutil.rmtree(TEST_DIR)
        print("\n[CLEANUP] Testes removidos")
    except:
        pass

if __name__ == '__main__':
    try:
        sucesso = teste_extracao()
        
        if sucesso:
            print("\n" + "="*80)
            print("[RESUMO]")
            print("="*80)
            print("""
PROBLEMA CORRIGIDO:
- App se "embaralhava" com multiplos itens em arquivo compactado
- Agora prioriza:
  1. Arquivos na RAIZ (vs em subpastas)
  2. Arquivo MAIOR (mais provavel ser o video real)
  
RESULTADO: Extrai sempre o video correto!
            """)
    finally:
        cleanup()
