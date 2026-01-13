#!/usr/bin/env python3
"""
Gerenciador de download de arquivos a partir de URLs
Suporta: Google Drive, MediaFire, links diretos, BackBlaze B2, etc
Com fallback inteligente que abre o navegador e clica em botões de download
"""

import aiohttp
import os
import re
import logging
import asyncio
import unicodedata
import subprocess
from urllib.parse import urlparse, parse_qs
from pathlib import Path

try:
    from browser_downloader import download_com_browser, BrowserDownloader
except ImportError:
    download_com_browser = None
    BrowserDownloader = None

log = logging.getLogger(__name__)

UPLOADS_DIR = "/opt/smindeck-bot/uploads"
if os.name == 'nt':
    UPLOADS_DIR = "uploads"

# Garantir que a pasta existe
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Extensões de arquivo permitidas
ALLOWED_EXTENSIONS = {
    # Vídeos
    'mp4', 'mkv', 'avi', 'mov', 'flv', 'wmv', 'webm', 'm4v',
    # Imagens
    'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'tiff',
    # Áudio
    'mp3', 'wav', 'aac', 'flac', 'm4a', 'ogg',
    # Tudo mais (bin, etc)
    'bin', 'unknown'
}

MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB


def validar_extensao(filename: str) -> bool:
    """Valida se o arquivo tem extensão permitida"""
    ext = filename.split('.')[-1].lower()
    # Agora aceita tudo - o importante é o arquivo estar lá
    return True


def gerar_nome_arquivo(url: str, index: int = 0, content_type: str = "") -> str:
    """
    Gera nome de arquivo único a partir da URL
    
    Args:
        url: URL do arquivo
        index: Índice do botão (0-11)
        content_type: Content-Type da resposta HTTP
    
    Returns:
        Nome de arquivo único
    """
    # Extrair nome original da URL
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)
    
    # Se não houver nome, tentar extrair extensão do URL ou usar Content-Type
    if not filename or filename == '':
        # Gerar nome baseado no tipo de arquivo do Content-Type
        ext = ".bin"
        
        if content_type:
            # Mapear Content-Type para extensão
            type_map = {
                'video/mp4': '.mp4',
                'video/x-matroska': '.mkv',
                'video/quicktime': '.mov',
                'video/x-msvideo': '.avi',
                'image/jpeg': '.jpg',
                'image/png': '.png',
                'image/gif': '.gif',
                'image/webp': '.webp',
                'audio/mpeg': '.mp3',
                'audio/wav': '.wav',
                'audio/x-wav': '.wav',
                'audio/aac': '.aac',
                'application/zip': '.zip',
                'application/x-rar-compressed': '.rar',
                'application/x-7z-compressed': '.7z',
            }
            
            # Procurar tipo correspondente
            for ct, e in type_map.items():
                if ct in content_type.lower():
                    ext = e
                    break
            
            # Se não encontrou no mapa, tentar extrair do content type
            if ext == ".bin":
                # Procurar padrão "video/", "image/", "audio/" etc
                if 'video/' in content_type.lower():
                    ext = '.mp4'  # Default para video
                elif 'image/' in content_type.lower():
                    ext = '.jpg'  # Default para imagem
                elif 'audio/' in content_type.lower():
                    ext = '.mp3'  # Default para áudio
        
        filename = f"botao_{index}{ext}"
    
    # Remover caracteres inválidos e acentos
    # Converter acentos para ASCII
    import unicodedata
    filename = unicodedata.normalize('NFKD', filename)
    filename = filename.encode('ascii', 'ignore').decode('ascii')
    
    # Remover caracteres inválidos
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Limitar tamanho do nome
    name, ext = os.path.splitext(filename)
    if len(name) > 50:
        name = name[:50]
    filename = name + ext
    
    return filename


async def download_google_drive(url: str) -> str | None:
    """
    Extrai link de download direto do Google Drive com múltiplas estratégias
    URLs do tipo: https://drive.google.com/file/d/{FILE_ID}/view
    
    Returns:
        Link direto de download ou None
    """
    try:
        # Extrair FILE_ID - suporta múltiplos formatos
        match = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
        if not match:
            # Tentar outro padrão
            match = re.search(r'id=([a-zA-Z0-9-_]+)', url)
            if not match:
                return None
        
        file_id = match.group(1)
        
        # ✅ Estratégia 1: Usar /uc?export=download (funciona melhor)
        direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        
        return direct_url
    except Exception as e:
        log.error(f"❌ Erro ao processar Google Drive: {e}")
        return None


async def download_mediafire(url: str) -> str | None:
    """
    Faz parse do MediaFire para extrair link de download direto
    URLs do tipo: https://www.mediafire.com/file/{KEY}/
    
    Returns:
        Link direto de download ou None
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    return None
                
                html = await resp.text()
                
                # Procurar padrão de link direto no HTML
                match = re.search(r'"(https://download\d+\.mediafire\.com/[^"]+)"', html)
                if match:
                    return match.group(1)
                
                # Alternativa: procurar por "aria-label" ou outro padrão
                match = re.search(r'href="(https://[^"]*download[^"]*mediafire[^"]*)"', html)
                if match:
                    return match.group(1)
                
                return None
    except Exception as e:
        log.error(f"❌ Erro ao processar MediaFire: {e}")
        return None


async def download_arquivo(url: str, filename: str, index: int = 0) -> str | None:
    """
    Faz download de um arquivo a partir de uma URL
    
    Suporta:
    - Google Drive
    - MediaFire
    - BackBlaze B2 (f000.backblazeb2.com)
    - Links diretos (HTTP/HTTPS)
    - Dropbox, OneDrive, etc (links diretos)
    - Qualquer servidor HTTP/HTTPS
    
    Args:
        url: URL do arquivo
        filename: Nome para salvar o arquivo
        index: Índice do botão (0-11)
    
    Returns:
        Caminho do arquivo baixado ou None se falhar
    """
    
    output_path = None
    
    try:
        # Validar URL
        if not url.startswith(('http://', 'https://')):
            log.error(f"❌ URL inválida: {url}")
            return None
        
        download_url = url
        
        # Processar URLs especiais
        if 'drive.google.com' in url:
            log.info("📥 Processando Google Drive...")
            # Usar método específico para Google Drive
            if BrowserDownloader:
                try:
                    downloader = BrowserDownloader(headless=True)
                    if await downloader.initialize():
                        result = await downloader.download_google_drive(url, filename)
                        await downloader.close()
                        if result:
                            log.info(f"✅ Google Drive download bem-sucedido: {result}")
                            return result
                except Exception as e:
                    log.error(f"❌ Erro ao usar Google Drive downloader: {e}")
            
            # Fallback: tentar extrair link direto
            download_url = await download_google_drive(url)
            if not download_url:
                log.error("❌ Não foi possível extrair link do Google Drive")
                return None
        
        elif 'mediafire.com' in url:
            log.info("📥 Processando MediaFire...")
            download_url = await download_mediafire(url)
            if not download_url:
                log.error("❌ Não foi possível extrair link do MediaFire")
                return None
        
        # Gerar nome de arquivo se não fornecido
        if not filename or filename == '':
            filename = gerar_nome_arquivo(download_url, index)
        
        # Validar extensão - se não for válida, tentar detectar ou usar fallback
        extension_valid = validar_extensao(filename)
        
        if not extension_valid:
            log.warning(f"⚠️ Extensão não detectada: {filename}")
            log.info("🤖 Vamos tentar com o browser...")
            
            # Tentar com browser sem validação prévia
            if download_com_browser:
                try:
                    log.info("🌐 Abrindo navegador para download automático...")
                    result = await asyncio.to_thread(
                        lambda: asyncio.run(download_com_browser(url, gerar_nome_arquivo(url, index, "video/mp4"), headless=True))
                    )
                    
                    if result and os.path.exists(result):
                        log.info(f"✅ Download com browser bem-sucedido: {result}")
                        return result
                except Exception as e:
                    log.warning(f"⚠️ Browser downloader falhou: {e}")
            
            log.error(f"❌ Não foi possível fazer download do arquivo")
            return None
        
        # Caminho de destino
        output_path = os.path.join(UPLOADS_DIR, filename)
        
        log.info(f"📥 Iniciando download: {download_url}")
        log.info(f"💾 Salvando em: {output_path}")
        
        # Múltiplas tentativas de download com diferentes headers
        # 🔴 Para Google Drive, precisamos de headers especiais
        if 'drive.google.com' in url or 'uc?export=download' in download_url:
            headers_list = [
                {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Referer': 'https://drive.google.com/'},
                {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Referer': 'https://drive.google.com/'},
                {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'},
                {'User-Agent': 'curl/7.68.0'},
            ]
        else:
            headers_list = [
                {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'},
                {'User-Agent': 'VLC/3.0.0'},
                {'User-Agent': 'ffmpeg/4.0'},
            ]
        
        downloaded = False
        last_error = None
        
        for attempt, headers in enumerate(headers_list, 1):
            try:
                log.info(f"⏳ Tentativa {attempt}/{len(headers_list)}...")
                
                async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=300),
                    connector=aiohttp.TCPConnector(ssl=False)
                ) as session:
                    # Para Google Drive, pode precisar de cookie de bypass
                    params = {}
                    if 'uc?export=download' in download_url:
                        params = {'confirm': 't'}  # Bypass de confirmação de vírus
                    
                    async with session.get(
                        download_url,
                        headers=headers,
                        params=params,
                        ssl=False,
                        allow_redirects=True
                    ) as resp:
                        
                        if resp.status == 200:
                            # Verificar tamanho
                            content_length = resp.content_length
                            if content_length and content_length > MAX_FILE_SIZE:
                                log.error(f"❌ Arquivo muito grande: {content_length / 1024 / 1024:.2f}MB (máx 500MB)")
                                return None
                            
                            # Fazer download em chunks
                            downloaded_size = 0
                            with open(output_path, 'wb') as f:
                                async for chunk in resp.content.iter_chunked(8192):
                                    f.write(chunk)
                                    downloaded_size += len(chunk)
                                    
                                    # Verificar tamanho durante download
                                    if downloaded_size > MAX_FILE_SIZE:
                                        os.remove(output_path)
                                        log.error(f"❌ Arquivo excedeu tamanho máximo durante download")
                                        return None
                                    
                                    # Log de progresso
                                    if content_length and downloaded_size % (1024 * 1024) == 0:
                                        percent = (downloaded_size / content_length) * 100
                                        mb_down = downloaded_size / 1024 / 1024
                                        mb_total = content_length / 1024 / 1024
                                        log.info(f"⏳ Progresso: {mb_down:.1f}MB / {mb_total:.1f}MB ({percent:.1f}%)")
                            
                            downloaded = True
                            break
                        
                        elif resp.status == 404:
                            last_error = f"Arquivo não encontrado (404)"
                            log.warning(f"⚠️ {last_error}")
                            break  # Não tentar novamente com 404
                        
                        elif resp.status in [403, 401]:
                            last_error = f"Acesso negado ({resp.status})"
                            log.warning(f"⚠️ {last_error}")
                            break  # Não tentar novamente com erro de auth
                        
                        else:
                            last_error = f"HTTP {resp.status}"
                            log.warning(f"⚠️ Erro HTTP {resp.status}, tentando novamente...")
                
            except asyncio.TimeoutError:
                last_error = "Timeout"
                log.warning(f"⚠️ Timeout na tentativa {attempt}/{len(headers_list)}")
                continue
            
            except Exception as e:
                last_error = str(e)
                log.warning(f"⚠️ Erro na tentativa {attempt}/{len(headers_list)}: {e}")
                continue
        
        if not downloaded:
            if os.path.exists(output_path):
                os.remove(output_path)
            
            # 🤖 FALLBACK INTELIGENTE: Usar browser para simular cliques
            log.info("🤖 Download direto falhou, tentando com browser inteligente...")
            
            if download_com_browser:
                try:
                    log.info("🌐 Abrindo navegador para procurar botão de download...")
                    result = await asyncio.to_thread(
                        lambda: asyncio.run(download_com_browser(url, filename, headless=True))
                    )
                    
                    if result and os.path.exists(result):
                        log.info(f"✅ Download com browser bem-sucedido: {result}")
                        return result
                except Exception as e:
                    log.warning(f"⚠️ Browser downloader falhou: {e}")
            
            log.error(f"❌ Falha no download após {len(headers_list)} tentativas. Último erro: {last_error}")
            return None
        
        file_size = os.path.getsize(output_path)
        log.info(f"✅ Download concluído: {filename} ({file_size / 1024 / 1024:.2f}MB)")
        
        return output_path
        
    except Exception as e:
        log.error(f"❌ Erro ao fazer download: {e}")
        import traceback
        log.error(traceback.format_exc())
        if output_path and os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass
        return None


async def validar_url(url: str) -> bool:
    """Valida se a URL é acessível e contém um arquivo válido"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        async with aiohttp.ClientSession() as session:
            async with session.head(
                url,
                timeout=aiohttp.ClientTimeout(total=10),
                headers=headers,
                ssl=False,
                allow_redirects=True
            ) as resp:
                # Verificar status
                if resp.status not in [200, 206]:
                    return False
                
                # Verificar Content-Type (opcional)
                content_type = resp.headers.get('Content-Type', '')
                
                return True
    except Exception as e:
        log.error(f"❌ Erro ao validar URL: {e}")
        return False
