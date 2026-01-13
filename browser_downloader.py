#!/usr/bin/env python3
"""
🤖 Browser Downloader - Inteligência Artificial de Download
Abre o navegador, procura pelos botões de download e simula cliques
Suporta: Google Drive, MediaFire, Dropbox, OneDrive, qualquer site com botão de download
"""

import asyncio
import logging
import os
from pathlib import Path

try:
    from playwright.async_api import async_playwright, Page
except ImportError:
    async_playwright = None
    Page = None

log = logging.getLogger(__name__)

DOWNLOADS_DIR = "/opt/smindeck-bot/uploads"
if os.name == 'nt':
    DOWNLOADS_DIR = "uploads"

# Garantir que a pasta existe
os.makedirs(DOWNLOADS_DIR, exist_ok=True)


class BrowserDownloader:
    """Downloader inteligente que simula cliques em botões de download"""
    
    def __init__(self, headless: bool = True):
        """
        Inicializa o browser downloader
        
        Args:
            headless: Se True, executa sem mostrar a janela do navegador
        """
        self.headless = headless
        self.playwright = None
        self.browser = None
    
    async def initialize(self):
        """Inicializa o Playwright e o navegador"""
        if async_playwright is None:
            log.error("❌ Playwright não está instalado! Instale com: pip install playwright")
            return False
        
        try:
            self.playwright = await async_playwright().start()
            
            # Usar Chromium (mais estável)
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                ]
            )
            
            log.info("✅ Navegador iniciado com sucesso")
            return True
        except Exception as e:
            log.error(f"❌ Erro ao inicializar navegador: {e}")
            return False
    
    async def close(self):
        """Fecha o navegador"""
        try:
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            log.info("✅ Navegador fechado")
        except Exception as e:
            log.error(f"❌ Erro ao fechar navegador: {e}")
    
    async def download_google_drive(self, url: str, output_filename: str) -> str | None:
        """
        Baixa arquivo do Google Drive extraindo o link direto
        Evita o bloqueio de downloads automatizados do Drive
        """
        page = None
        try:
            # Extrair ID do arquivo
            file_id = None
            if '/file/d/' in url:
                file_id = url.split('/file/d/')[1].split('/')[0]
            elif '?id=' in url:
                file_id = url.split('?id=')[1].split('&')[0]
            
            if not file_id:
                log.warning("❌ Não consegui extrair ID do Google Drive")
                return None
            
            log.info(f"📝 ID do arquivo: {file_id}")
            
            import aiohttp
            
            # Estratégia 1: Tentar com sessão e cookies
            async with aiohttp.ClientSession() as session:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                
                # Preparar URLs para tentar (em ordem de prioridade)
                urls_to_try = [
                    # Força download direto com confirmação
                    f"https://drive.google.com/uc?export=download&id={file_id}&confirm=yes",
                    f"https://drive.google.com/uc?export=download&id={file_id}&confirm=t",
                    # URL sem confirmação
                    f"https://drive.google.com/uc?export=download&id={file_id}",
                    # URL alternativa
                    f"https://drive-thirdparty.googleusercontent.com/download?id={file_id}",
                ]
                
                for direct_url in urls_to_try:
                    try:
                        log.info(f"🔗 Tentando: {direct_url[:80]}...")
                        
                        async with session.get(direct_url, headers=headers, timeout=aiohttp.ClientTimeout(total=60), allow_redirects=True, ssl=False) as resp:
                            if resp.status == 200:
                                content = await resp.content.read()
                                
                                # Verificar tamanho (HTML aviso é sempre pequenininho ~2KB)
                                if len(content) < 5000 and (content[:50].startswith(b'<!DOCTYPE') or content[:100].startswith(b'<html')):
                                    log.warning(f"⚠️ Resposta é HTML (tamanho: {len(content)}), não arquivo binário")
                                    continue
                                
                                # Detectar Content-Type
                                content_type = resp.headers.get('Content-Type', 'application/octet-stream').lower()
                                
                                log.info(f"✅ Download bem-sucedido! Tamanho: {len(content)} bytes, Type: {content_type}")
                                
                                # Se o filename tem .bin, tentar detectar extensão correta
                                if output_filename.endswith('.bin'):
                                    # Mapa de Content-Type para extensão
                                    type_map = {
                                        'video/mp4': '.mp4',
                                        'video/x-matroska': '.mkv',
                                        'video/quicktime': '.mov',
                                        'video/x-msvideo': '.avi',
                                        'video/webm': '.webm',
                                        'image/jpeg': '.jpg',
                                        'image/png': '.png',
                                        'image/gif': '.gif',
                                        'image/webp': '.webp',
                                        'audio/mpeg': '.mp3',
                                        'audio/wav': '.wav',
                                        'audio/aac': '.aac',
                                        'application/zip': '.zip',
                                        'application/x-rar-compressed': '.rar',
                                        'application/x-7z-compressed': '.7z',
                                        'application/pdf': '.pdf',
                                    }
                                    
                                    # Procurar extensão pelo Content-Type
                                    ext = None
                                    for ct, e in type_map.items():
                                        if ct in content_type:
                                            ext = e
                                            break
                                    
                                    # Se não encontrou, tentar parse geral
                                    if not ext:
                                        if 'video/' in content_type:
                                            ext = '.mp4'
                                        elif 'image/' in content_type:
                                            ext = '.jpg'
                                        elif 'audio/' in content_type:
                                            ext = '.mp3'
                                        else:
                                            ext = '.bin'
                                    
                                    output_filename = output_filename[:-4] + ext  # Replace .bin with detected ext
                                
                                # Salvar arquivo
                                output_path = os.path.join(self.download_dir, output_filename)
                                with open(output_path, 'wb') as f:
                                    f.write(content)
                                
                                log.info(f"✅ Arquivo salvo: {output_path}")
                                return output_path
                        
                    except Exception as e:
                        log.warning(f"⚠️ Falha com URL {direct_url[:80]}: {e}")
                        continue
            
            # Se chegou aqui, todas as URLs falharam
            log.error("❌ Não consegui baixar do Google Drive por nenhuma estratégia")
            return None
        
        except Exception as e:
            log.error(f"❌ Erro ao baixar do Google Drive: {e}")
            return None
        finally:
            if page:
                await page.close()

    async def download_with_click(self, url: str, output_filename: str) -> str | None:
        """
        Abre uma URL e procura por botões de download
        Simula cliques em botões e captura o arquivo baixado
        
        Args:
            url: URL da página
            output_filename: Nome do arquivo para salvar
        
        Returns:
            Caminho do arquivo ou None se falhar
        """
        
        page = None
        try:
            # Criar contexto com diretório de download
            context = await self.browser.new_context(
                accept_downloads=True,
            )
            
            page = await context.new_page()
            
            # Somar timeout
            page.set_default_timeout(30000)  # 30 segundos
            page.set_default_navigation_timeout(30000)
            
            log.info(f"🌐 Abrindo URL: {url}")
            
            try:
                await page.goto(url, wait_until="networkidle")
            except Exception as e:
                log.warning(f"⚠️  Timeout ao carregar página: {e}")
                # Continuar mesmo com timeout
            
            # Aguardar página carregar um pouco
            await asyncio.sleep(2)
            
            # 🎯 Procurar e clicar em botão de download
            download_button = await self._find_download_button(page)
            
            if not download_button:
                log.warning("⚠️  Nenhum botão de download encontrado")
                await context.close()
                return None
            
            log.info("🖱️  Botão de download encontrado, simulando clique...")
            
            # Aguardar download
            async with page.expect_download() as download_info:
                await download_button.click()
                download = await download_info.value
                
                # Aguardar o arquivo ser baixado
                await download.path()
                
                # Obter o nome original do arquivo
                original_name = download.suggested_filename
                source_path = await download.path()
                
                # Caminho de destino
                dest_path = os.path.join(DOWNLOADS_DIR, output_filename)
                
                # Copiar arquivo para o destino
                import shutil
                shutil.copy(str(source_path), dest_path)
                
                log.info(f"✅ Download concluído: {dest_path}")
                
                await context.close()
                return dest_path
        
        except Exception as e:
            log.error(f"❌ Erro ao fazer download: {e}")
            if page:
                try:
                    await page.close()
                except:
                    pass
            return None
    
    async def _find_download_button(self, page: Page):
        """
        Procura por botão de download na página
        Tenta vários seletores e textos comuns
        """
        
        # Padrões a procurar
        selectors = [
            # Google Drive
            'a[href*="download"]',
            'button:has-text("Download")',
            'button:has-text("Baixar")',
            
            # MediaFire
            'a.download_link',
            'a#downloadButton',
            'button:has-text("Click here")',
            
            # Dropbox
            'a[href*="/download"]',
            'button:has-text("Download")',
            
            # Genéricos
            '[data-testid*="download"]',
            '[aria-label*="download" i]',
            '[aria-label*="baixar" i]',
            'a:has-text("download")',
            'a:has-text("Download")',
            'a:has-text("Baixar")',
            'button:has-text("download")',
            'button:has-text("Baixar")',
            'input[type="button"][value*="Download"]',
        ]
        
        for selector in selectors:
            try:
                log.info(f"🔍 Procurando: {selector}")
                element = await page.query_selector(selector)
                
                if element:
                    # Verificar se é visível
                    is_visible = await element.is_visible()
                    if is_visible:
                        log.info(f"✅ Encontrado: {selector}")
                        return element
            except Exception as e:
                log.debug(f"⚠️  Erro ao procurar {selector}: {e}")
                continue
        
        # Fallback: procurar por qualquer link/botão contendo "download" ou "baixar"
        try:
            # JavaScript para procurar elementos
            script = """
            () => {
                const keywords = ['download', 'baixar', 'click here', 'get'];
                const elements = Array.from(document.querySelectorAll('a, button'));
                
                for (const el of elements) {
                    const text = el.textContent.toLowerCase();
                    const href = el.getAttribute('href') || '';
                    const dataUrl = el.getAttribute('data-url') || '';
                    
                    if (keywords.some(kw => 
                        text.includes(kw) || 
                        href.includes('download') || 
                        dataUrl.includes('download')
                    )) {
                        return el;
                    }
                }
                return null;
            }
            """
            
            element_handle = await page.evaluate_handle(script)
            element = await element_handle.as_element()
            
            if element:
                log.info("✅ Encontrado elemento de download via JavaScript")
                return element
        except Exception as e:
            log.debug(f"⚠️  Erro no fallback: {e}")
        
        return None
    
    async def extract_direct_link(self, page: Page) -> str | None:
        """
        Tenta extrair um link de download direto da página
        Útil para alguns sites que fornecem o URL diretamente
        """
        try:
            script = """
            () => {
                const links = Array.from(document.querySelectorAll('a'));
                const dlLinks = links.filter(a => {
                    const href = a.getAttribute('href') || '';
                    return href.match(/\\.(mp4|jpg|png|gif|zip|rar|7z|mkv|mov|avi)$/i);
                });
                return dlLinks[0]?.getAttribute('href') || null;
            }
            """
            
            link = await page.evaluate(script)
            if link:
                log.info(f"🔗 Link direto encontrado: {link}")
                return link
        except Exception as e:
            log.debug(f"⚠️  Erro ao extrair link: {e}")
        
        return None


async def download_com_browser(url: str, output_filename: str, headless: bool = True) -> str | None:
    """
    Função de conveniência para fazer download com browser
    
    Args:
        url: URL da página
        output_filename: Nome do arquivo para salvar
        headless: Se True, executa sem mostrar a janela
    
    Returns:
        Caminho do arquivo ou None se falhar
    """
    
    if async_playwright is None:
        log.error("❌ Playwright não instalado")
        return None
    
    downloader = BrowserDownloader(headless=headless)
    
    try:
        # Inicializar
        if not await downloader.initialize():
            return None
        
        # Fazer download
        result = await downloader.download_with_click(url, output_filename)
        
        return result
    
    finally:
        # Fechar sempre
        await downloader.close()


# Teste local
if __name__ == "__main__":
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    if len(sys.argv) < 2:
        print("Uso: python browser_downloader.py <URL> [output_filename]")
        sys.exit(1)
    
    url = sys.argv[1]
    output_filename = sys.argv[2] if len(sys.argv) > 2 else "arquivo_baixado.bin"
    
    # Executar teste
    result = asyncio.run(download_com_browser(url, output_filename, headless=False))
    
    if result:
        print(f"✅ Sucesso! Arquivo: {result}")
    else:
        print("❌ Falha no download")
