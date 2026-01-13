#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste rápido de download de URL
Para validar se a URL funciona antes de enviar ao bot
"""

import asyncio
import aiohttp
import os
from pathlib import Path

# URL que está falhando
TEST_URL = "https://f000.backblazeb2.com/file/deptos/mordomia/provaí-e-vede/2026/episódios/01-10-26_%20primícias-de-fe.mp4"

# User-Agents para testar
USER_AGENTS = [
    ("Mozilla (Windows)", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"),
    ("Mozilla (Linux)", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"),
    ("VLC", "VLC/3.0.0"),
    ("ffmpeg", "ffmpeg/4.0"),
]

async def test_url():
    print("=" * 70)
    print("🧪 TESTE DE URL - Download Manager")
    print("=" * 70)
    print(f"\n🔗 URL: {TEST_URL}\n")
    
    for name, ua in USER_AGENTS:
        print(f"\n{'='*70}")
        print(f"📝 Testando com: {name}")
        print(f"   User-Agent: {ua}")
        print(f"{'='*70}")
        
        try:
            headers = {'User-Agent': ua}
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                async with session.head(
                    TEST_URL,
                    headers=headers,
                    ssl=False,
                    allow_redirects=True
                ) as resp:
                    print(f"✅ Status: {resp.status}")
                    print(f"   Content-Type: {resp.headers.get('Content-Type', 'N/A')}")
                    print(f"   Content-Length: {resp.headers.get('Content-Length', 'N/A')} bytes")
                    
                    if resp.status == 200:
                        size_mb = int(resp.headers.get('Content-Length', 0)) / 1024 / 1024
                        print(f"   📊 Tamanho: {size_mb:.1f}MB")
                        print(f"\n   ✅ Este User-Agent funciona! Use este para download.")
                        return True
                    else:
                        print(f"   ❌ Status HTTP {resp.status} - não funciona com este UA")
        
        except asyncio.TimeoutError:
            print(f"   ❌ Timeout - Servidor demorando demais")
        except aiohttp.ClientSSLError:
            print(f"   ⚠️  Erro SSL - Tentando com ssl=False (já está configurado)")
        except aiohttp.ClientConnectorError as e:
            print(f"   ❌ Erro de conexão: {e}")
        except Exception as e:
            print(f"   ❌ Erro: {type(e).__name__}: {e}")
    
    print(f"\n{'='*70}")
    print("❌ NENHUM User-Agent funcionou!")
    print(f"{'='*70}")
    print("\nPossíveis soluções:")
    print("1. Verifique se a URL está correta")
    print("2. Verifique sua conexão de internet")
    print("3. O servidor pode estar fora do ar")
    print("4. Tente a URL diretamente no navegador")
    return False

async def test_download():
    """Teste de download real"""
    print(f"\n{'='*70}")
    print("📥 TESTE DE DOWNLOAD REAL")
    print(f"{'='*70}")
    
    output_file = "teste_download.mp4"
    
    # Usar o User-Agent que funcionou (Mozilla Windows)
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    try:
        headers = {'User-Agent': ua}
        
        print(f"\n⏳ Iniciando download em: {output_file}")
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=300)) as session:
            async with session.get(
                TEST_URL,
                headers=headers,
                ssl=False,
                allow_redirects=True
            ) as resp:
                
                if resp.status != 200:
                    print(f"❌ Erro HTTP {resp.status}")
                    return False
                
                content_length = resp.content_length
                downloaded = 0
                
                with open(output_file, 'wb') as f:
                    async for chunk in resp.content.iter_chunked(65536):
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if content_length:
                            percent = (downloaded / content_length) * 100
                            mb_down = downloaded / 1024 / 1024
                            mb_total = content_length / 1024 / 1024
                            print(f"⏳ {mb_down:.1f}MB / {mb_total:.1f}MB ({percent:.1f}%)")
        
        # Verificar arquivo
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print(f"\n✅ Download concluído!")
            print(f"   Arquivo: {output_file}")
            print(f"   Tamanho: {size / 1024 / 1024:.1f}MB")
            
            # Limpar
            os.remove(output_file)
            print(f"   (arquivo removido)")
            return True
        
    except Exception as e:
        print(f"❌ Erro: {type(e).__name__}: {e}")
        if os.path.exists(output_file):
            os.remove(output_file)
        return False

async def main():
    print("\n")
    
    # Teste HEAD (rápido)
    success = await test_url()
    
    if success:
        # Teste GET (completo) - opcional
        try:
            resp = await asyncio.wait_for(test_download(), timeout=60)
            if resp:
                print("\n" + "="*70)
                print("🎉 SUCESSO TOTAL!")
                print("="*70)
                print("\nA URL está funcionando e pode ser enviada ao bot!")
                print("\nNo Discord:")
                print("1. Envie 'oi'")
                print("2. Escolha tipo (Vídeo/Imagem)")
                print("3. Escolha botão")
                print("4. Envie a URL")
        except asyncio.TimeoutError:
            print("\n⏳ Download demorou demais (pulando teste de download)")
            print("\n✅ URL respondendo bem!")
            print("Você pode enviar para o bot agora.")

if __name__ == "__main__":
    asyncio.run(main())
