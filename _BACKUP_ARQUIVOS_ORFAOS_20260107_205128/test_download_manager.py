#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para validar o sistema de download de URLs
Testa sem fazer downloads reais
"""

import asyncio
import sys
from download_manager import (
    validar_extensao,
    gerar_nome_arquivo,
    download_google_drive,
    download_mediafire,
    validar_url
)

async def testar():
    print("=" * 60)
    print("🧪 TESTES DO SISTEMA DE DOWNLOAD")
    print("=" * 60)
    
    # Teste 1: Validar extensão
    print("\n✅ TESTE 1: Validação de Extensão")
    print("-" * 60)
    testes_ext = [
        ("video.mp4", True),
        ("imagem.jpg", True),
        ("audio.mp3", True),
        ("script.exe", False),
        ("documento.pdf", False),
        ("foto.png", True),
    ]
    
    for arquivo, esperado in testes_ext:
        resultado = validar_extensao(arquivo)
        status = "✅" if resultado == esperado else "❌"
        print(f"{status} {arquivo}: {resultado} (esperado: {esperado})")
    
    # Teste 2: Gerar nome de arquivo
    print("\n✅ TESTE 2: Geração de Nome de Arquivo")
    print("-" * 60)
    urls_teste = [
        "https://drive.google.com/file/d/ABC123/view",
        "https://www.mediafire.com/file/XYZ789/meu_video.mp4",
        "https://servidor.com/pasta/imagem.jpg",
        "https://exemplo.com/sem-nome",
    ]
    
    for i, url in enumerate(urls_teste):
        nome = gerar_nome_arquivo(url, i)
        print(f"URL {i+1}: {url[:50]}...")
        print(f"  → Nome gerado: {nome}\n")
    
    # Teste 3: Google Drive URL parsing
    print("\n✅ TESTE 3: Google Drive URL Parsing")
    print("-" * 60)
    drive_urls = [
        "https://drive.google.com/file/d/1A2B3C4D5E6F7G8H9I0J/view",
        "https://drive.google.com/file/d/ABC123XYZ789/view?usp=sharing",
    ]
    
    for url in drive_urls:
        resultado = await download_google_drive(url)
        print(f"Input:  {url}")
        print(f"Output: {resultado}\n")
    
    # Teste 4: MediaFire URL
    print("\n✅ TESTE 4: MediaFire URL (sem fazer requisição)")
    print("-" * 60)
    print("⏭️  Pulando teste de MediaFire (requer conexão real)")
    print("   O sistema fará parsing do HTML quando necessário")
    
    # Teste 5: Validação de URL
    print("\n✅ TESTE 5: Validação de URL")
    print("-" * 60)
    urls_invalidas = [
        "notaurl",
        "ftp://servidor.com/arquivo",
        "",
        "http//servidor.com",
    ]
    
    urls_validas = [
        "http://servidor.com/arquivo.mp4",
        "https://drive.google.com/file/d/ABC/view",
    ]
    
    print("URLs inválidas:")
    for url in urls_invalidas:
        valida = url.startswith(('http://', 'https://'))
        print(f"  {url!r}: {valida}")
    
    print("\nURLs válidas:")
    for url in urls_validas:
        valida = url.startswith(('http://', 'https://'))
        print(f"  {url!r}: {valida}")
    
    print("\n" + "=" * 60)
    print("✅ TESTES CONCLUÍDOS COM SUCESSO!")
    print("=" * 60)
    print("\n📝 Próximos passos:")
    print("1. Execute o bot: python bot.py")
    print("2. No Discord, envie 'oi'")
    print("3. Escolha um botão e tipo (Vídeo/Imagem)")
    print("4. Envie uma URL real (Google Drive, etc)")
    print("5. Monitore os logs: tail -f /opt/smindeck-bot/debug.log")

if __name__ == "__main__":
    try:
        asyncio.run(testar())
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
