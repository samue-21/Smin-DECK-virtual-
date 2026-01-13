#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para a funcionalidade de YouTube no SminDeck
"""

import sys
import re
import webbrowser

# Simular as funções principais
def is_youtube_url(url_string):
    """Verifica se a string é uma URL válida do YouTube"""
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
    return bool(re.match(youtube_regex, url_string))

def extract_youtube_id(url):
    """Extrai o ID do vídeo da URL do YouTube"""
    try:
        match = re.search(r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)', url)
        if match:
            return match.group(1)
    except Exception as e:
        print(f"❌ Erro ao extrair ID do YouTube: {e}")
    return None

def test_urls():
    """Testa várias URLs do YouTube"""
    test_cases = [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", True, "dQw4w9WgXcQ"),
        ("https://youtu.be/dQw4w9WgXcQ", True, "dQw4w9WgXcQ"),
        ("https://www.youtube.com/embed/dQw4w9WgXcQ", True, "dQw4w9WgXcQ"),
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=10s", True, "dQw4w9WgXcQ"),
        ("youtube.com/watch?v=dQw4w9WgXcQ", True, "dQw4w9WgXcQ"),
        ("https://example.com", False, None),
        ("file.mp4", False, None),
    ]
    
    print("=" * 60)
    print("🧪 Teste de URLs do YouTube")
    print("=" * 60)
    
    for url, should_be_valid, expected_id in test_cases:
        is_valid = is_youtube_url(url)
        video_id = extract_youtube_id(url) if is_valid else None
        
        status = "✅" if (is_valid == should_be_valid and video_id == expected_id) else "❌"
        print(f"\n{status} URL: {url}")
        print(f"   Válida: {is_valid} (esperado: {should_be_valid})")
        print(f"   ID: {video_id} (esperado: {expected_id})")

if __name__ == "__main__":
    test_urls()
    print("\n" + "=" * 60)
    print("✅ Testes concluídos!")
    print("=" * 60)
