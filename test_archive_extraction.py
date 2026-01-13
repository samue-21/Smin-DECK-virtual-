#!/usr/bin/env python3
"""
Script de teste para a funcionalidade de extração de arquivos compactados
Testa arquivo_processor.py com exemplos de ZIP
"""

import os
import sys
import tempfile
import zipfile
from pathlib import Path

# Adicionar diretório do projeto ao PATH
sys.path.insert(0, os.path.dirname(__file__))

# Simular UPLOADS_DIR
os.environ['UPLOADS_DIR'] = os.path.join(tempfile.gettempdir(), 'smindeckbot_test')
os.makedirs(os.environ['UPLOADS_DIR'], exist_ok=True)

from arquivo_processor import extrair_arquivo_compactado, eh_arquivo_compactado

def criar_arquivo_teste(pasta_temp: str, tipo_arquivo: str) -> str:
    """Cria arquivo de teste para simulação"""
    if tipo_arquivo == 'video':
        arquivo = os.path.join(pasta_temp, 'video_teste.mp4')
        with open(arquivo, 'wb') as f:
            f.write(b'teste_video_content_' * 100)
        return arquivo
    elif tipo_arquivo == 'imagem':
        arquivo = os.path.join(pasta_temp, 'imagem_teste.jpg')
        with open(arquivo, 'wb') as f:
            f.write(b'fake_jpeg_header_' * 50)
        return arquivo
    elif tipo_arquivo == 'audio':
        arquivo = os.path.join(pasta_temp, 'audio_teste.mp3')
        with open(arquivo, 'wb') as f:
            f.write(b'fake_mp3_header_' * 50)
        return arquivo

def teste_extracacao_zip():
    """Testa extração de arquivo ZIP com múltiplos arquivos"""
    print("\n" + "="*60)
    print("TESTE 1: Extração de ZIP com múltiplos arquivos")
    print("="*60)
    
    # Criar ZIP com vários arquivos
    with tempfile.TemporaryDirectory() as temp_dir:
        # Criar arquivos de teste
        video_path = criar_arquivo_teste(temp_dir, 'video')
        imagem_path = criar_arquivo_teste(temp_dir, 'imagem')
        audio_path = criar_arquivo_teste(temp_dir, 'audio')
        
        # Criar ZIP
        zip_path = os.path.join(temp_dir, 'teste.zip')
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.write(video_path, arcname='video.mp4')
            zf.write(imagem_path, arcname='imagem.jpg')
            zf.write(audio_path, arcname='audio.mp3')
            # Adicionar arquivo inútil
            zf.writestr('readme.txt', 'Este é um arquivo de teste')
        
        print(f"\n✅ ZIP criado: {zip_path}")
        print(f"✅ Tamanho: {os.path.getsize(zip_path)} bytes")
        
        # Testar detecção
        print(f"\n📦 Testando detecção de arquivo compactado...")
        eh_compactado = eh_arquivo_compactado(zip_path)
        print(f"{'✅' if eh_compactado else '❌'} eh_arquivo_compactado('{os.path.basename(zip_path)}'): {eh_compactado}")
        
        # Testar extração de vídeo
        print(f"\n🎬 Testando extração de vídeo...")
        arquivo_extraido = extrair_arquivo_compactado(zip_path, 'video')
        if arquivo_extraido:
            print(f"✅ Vídeo extraído: {arquivo_extraido}")
            print(f"   Tamanho: {os.path.getsize(arquivo_extraido)} bytes")
            assert os.path.exists(arquivo_extraido), "Arquivo extraído não existe!"
        else:
            print(f"❌ Falha na extração de vídeo")
            return False
        
        # Testar extração de imagem
        print(f"\n🖼️ Testando extração de imagem...")
        arquivo_extraido = extrair_arquivo_compactado(zip_path, 'imagem')
        if arquivo_extraido:
            print(f"✅ Imagem extraída: {arquivo_extraido}")
            print(f"   Tamanho: {os.path.getsize(arquivo_extraido)} bytes")
        else:
            print(f"❌ Falha na extração de imagem")
            return False
        
        # Testar extração de áudio
        print(f"\n🔊 Testando extração de áudio...")
        arquivo_extraido = extrair_arquivo_compactado(zip_path, 'audio')
        if arquivo_extraido:
            print(f"✅ Áudio extraído: {arquivo_extraido}")
            print(f"   Tamanho: {os.path.getsize(arquivo_extraido)} bytes")
        else:
            print(f"❌ Falha na extração de áudio")
            return False
    
    return True

def teste_deteccao_tipo():
    """Testa detecção de diferentes tipos de arquivo compactado"""
    print("\n" + "="*60)
    print("TESTE 2: Detecção de tipos de arquivo compactado")
    print("="*60)
    
    testes = [
        ('arquivo.zip', True),
        ('arquivo.rar', True),
        ('arquivo.7z', True),
        ('arquivo.tar.gz', False),  # Não suportado ainda
        ('arquivo.mp4', False),
        ('arquivo.jpg', False),
    ]
    
    for nome_arquivo, esperado in testes:
        resultado = eh_arquivo_compactado(nome_arquivo)
        status = '✅' if resultado == esperado else '❌'
        print(f"{status} eh_arquivo_compactado('{nome_arquivo}'): {resultado} (esperado: {esperado})")
        if resultado != esperado:
            return False
    
    return True

def teste_upload_dir():
    """Verifica se UPLOADS_DIR foi criado corretamente"""
    print("\n" + "="*60)
    print("TESTE 3: Diretório de uploads")
    print("="*60)
    
    upload_dir = os.environ.get('UPLOADS_DIR')
    print(f"📁 UPLOADS_DIR: {upload_dir}")
    print(f"{'✅' if os.path.exists(upload_dir) else '❌'} Diretório existe: {os.path.exists(upload_dir)}")
    
    # Listar arquivos criados
    if os.path.exists(upload_dir):
        arquivos = os.listdir(upload_dir)
        if arquivos:
            print(f"\n📋 Arquivos extraídos:")
            for arquivo in arquivos[:5]:  # Mostrar apenas os primeiros 5
                caminho = os.path.join(upload_dir, arquivo)
                tamanho = os.path.getsize(caminho) if os.path.isfile(caminho) else 'DIR'
                print(f"   - {arquivo} ({tamanho} bytes)")
            if len(arquivos) > 5:
                print(f"   ... e mais {len(arquivos) - 5} arquivo(s)")
    
    return True

if __name__ == '__main__':
    print("\n" + "█"*60)
    print("🧪 TESTES DE EXTRAÇÃO DE ARQUIVOS COMPACTADOS")
    print("█"*60)
    
    testes = [
        ("Detecção de tipo", teste_deteccao_tipo),
        ("Extração de ZIP", teste_extracacao_zip),
        ("Diretório de uploads", teste_upload_dir),
    ]
    
    resultados = {}
    for nome_teste, funcao_teste in testes:
        try:
            resultado = funcao_teste()
            resultados[nome_teste] = '✅ PASSOU' if resultado else '❌ FALHOU'
        except Exception as e:
            print(f"\n❌ ERRO em {nome_teste}: {e}")
            import traceback
            traceback.print_exc()
            resultados[nome_teste] = f'❌ ERRO: {str(e)}'
    
    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)
    for nome_teste, resultado in resultados.items():
        print(f"{resultado} - {nome_teste}")
    
    # Status geral
    todas_passaram = all('PASSOU' in r for r in resultados.values())
    if todas_passaram:
        print("\n✅ TODOS OS TESTES PASSARAM!")
        sys.exit(0)
    else:
        print("\n❌ ALGUNS TESTES FALHARAM!")
        sys.exit(1)
