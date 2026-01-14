#!/usr/bin/env python3
"""
Processa e otimiza arquivos de mídia
- MP4/MKV → reduz resolução e bitrate com ffmpeg
- JPG/PNG → redimensiona e comprime com PIL
"""

import os
import subprocess
import shutil
from pathlib import Path
from pathlib import Path
from PIL import Image
import logging

log = logging.getLogger(__name__)

UPLOADS_DIR = "/opt/smindeck-bot/uploads"
if os.name == 'nt':
    UPLOADS_DIR = "uploads"

# Garantir que a pasta existe
os.makedirs(UPLOADS_DIR, exist_ok=True)


def processar_video(arquivo_path: str, output_filename: str) -> str:
    """
    Otimiza vídeo MP4 com ffmpeg
    - Resolução: 720p
    - Bitrate: 2Mbps
    - Codec: libx264
    
    Args:
        arquivo_path: Caminho do arquivo original
        output_filename: Nome para salvar (ex: video_botao_5.mp4)
    
    Returns:
        Caminho do arquivo processado ou None se falhar
    """
    try:
        output_path = os.path.join(UPLOADS_DIR, output_filename)
        
        # Comando ffmpeg
        cmd = [
            'ffmpeg',
            '-i', arquivo_path,
            '-vf', 'scale=1280:720:force_original_aspect_ratio=decrease',  # 720p
            '-c:v', 'libx264',
            '-crf', '28',  # Qualidade (0-51, 28 é padrão)
            '-b:v', '2000k',  # Bitrate de vídeo
            '-c:a', 'aac',
            '-b:a', '128k',  # Bitrate de áudio
            '-y',  # Sobrescrever arquivo de saída
            output_path
        ]
        
        log.info(f"🎥 Compactando vídeo: {arquivo_path}")
        
        resultado = subprocess.run(cmd, capture_output=True, timeout=300)
        
        if resultado.returncode == 0 and os.path.exists(output_path):
            tamanho_original = os.path.getsize(arquivo_path) / (1024 * 1024)  # MB
            tamanho_final = os.path.getsize(output_path) / (1024 * 1024)  # MB
            compressao = (1 - tamanho_final / tamanho_original) * 100
            
            log.info(f"✅ Vídeo compactado: {tamanho_original:.1f}MB → {tamanho_final:.1f}MB ({compressao:.0f}%)")
            return output_path
        else:
            log.error(f"❌ Erro ao compactar vídeo: {resultado.stderr.decode()}")
            return None
    except Exception as e:
        log.error(f"❌ Erro processando vídeo: {e}")
        return None


def processar_imagem(arquivo_path: str, output_filename: str) -> str:
    """
    Otimiza imagem com PIL
    - Redimensiona para máx 1920x1080
    - Comprime para JPEG 85%
    
    Args:
        arquivo_path: Caminho do arquivo original
        output_filename: Nome para salvar (ex: imagem_botao_5.jpg)
    
    Returns:
        Caminho do arquivo processado ou None se falhar
    """
    try:
        output_path = os.path.join(UPLOADS_DIR, output_filename)
        
        img = Image.open(arquivo_path)
        
        # Redimensionar se muito grande
        max_width, max_height = 1920, 1080
        if img.width > max_width or img.height > max_height:
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            log.info(f"📐 Imagem redimensionada para {img.width}x{img.height}")
        
        # Converter para RGB se for PNG com alpha
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img
        
        # Salvar como JPEG otimizado
        img.save(output_path, 'JPEG', quality=85, optimize=True)
        
        tamanho_original = os.path.getsize(arquivo_path) / (1024 * 1024)
        tamanho_final = os.path.getsize(output_path) / (1024 * 1024)
        compressao = (1 - tamanho_final / tamanho_original) * 100
        
        log.info(f"✅ Imagem compactada: {tamanho_original:.1f}MB → {tamanho_final:.1f}MB ({compressao:.0f}%)")
        return output_path
    except Exception as e:
        log.error(f"❌ Erro processando imagem: {e}")
        return None


def processar_arquivo(arquivo_path: str, tipo: str, botao: int) -> str:
    """
    Processa arquivo genérico
    
    Fluxo especial para .bin do Google Drive:
    1. Detecta tipo real usando magic bytes
    2. Renomeia para extensão correta (.mp4, .png, etc)
    3. Processa o arquivo (reduz video, comprime imagem, etc)
    
    Args:
        arquivo_path: Caminho do arquivo enviado
        tipo: 'video', 'imagem'
        botao: Número do botão (0-11)
    
    Returns:
        Caminho do arquivo processado ou None
    """
    
    if not os.path.exists(arquivo_path):
        log.error(f"❌ Arquivo não encontrado: {arquivo_path}")
        return None
    
    # Se for .bin, detectar tipo real e renomear PRIMEIRO
    if arquivo_path.endswith('.bin'):
        extensao_real = _detect_bin_extension(arquivo_path)
        
        if extensao_real == '.bin':
            # Não conseguiu detectar - salvar como bin mesmo
            output_filename = f"{tipo}_botao_{botao}.bin"
            output_path = os.path.join(UPLOADS_DIR, output_filename)
            try:
                shutil.copy(arquivo_path, output_path)
                return output_path
            except Exception as e:
                return None
        
        # Conseguiu detectar tipo real - renomear e processar
        output_filename = f"{tipo}_botao_{botao}{extensao_real}"
        output_path = os.path.join(UPLOADS_DIR, output_filename)
        
        try:
            # Copiar com extensão correta
            shutil.copy(arquivo_path, output_path)
            
            # Agora processar o arquivo renomeado (reduzir video, comprimir imagem, etc)
            if tipo == 'video' and extensao_real.lower() in ['.mp4', '.mkv', '.webm', '.avi', '.mov']:
                return processar_video(output_path, output_filename)
            elif tipo == 'imagem' and extensao_real.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
                return processar_imagem(output_path, output_filename)
            else:
                # Não precisa processar (já está com extensão correta)
                return output_path
                
        except Exception as e:
            return None
    
    # Gerar nome de saída para arquivos que não são .bin
    extensao_map = {
        'video': 'mp4',
        'imagem': 'jpg'
    }
    ext = extensao_map.get(tipo, 'bin')
    output_filename = f"{tipo}_botao_{botao}.{ext}"
    
    # Processar
    if tipo == 'video':
        return processar_video(arquivo_path, output_filename)
    elif tipo == 'imagem':
        return processar_imagem(arquivo_path, output_filename)
    else:
        # Copiar arquivo sem processar
        output_path = os.path.join(UPLOADS_DIR, output_filename)
        shutil.copy(arquivo_path, output_path)
        log.info(f"📁 Arquivo copiado: {output_filename}")
        return output_path


def _detect_bin_extension(file_path: str) -> str:
    """
    Detecta a extensão real de um arquivo .bin usando magic bytes
    Essencial para arquivos do Google Drive que vêm como .bin
    
    Returns:
        Extensão com ponto (ex: .mp4) ou .bin como fallback
    """
    try:
        with open(file_path, 'rb') as f:
            magic_bytes = f.read(32)
        
        # ZIP / Arquivo compactado (Google Drive, etc)
        if magic_bytes[0:4] == b'PK\x03\x04':
            return '.zip'
        # Vídeo MP4 / M4A / MOV (ftyp é a signature)
        elif magic_bytes[4:8] == b'ftyp':
            # Verificar se é MP4, M4A ou outro formato ftyp
            if b'm4a' in magic_bytes[:20]:
                return '.m4a'
            elif b'qt  ' in magic_bytes[:20]:  # QuickTime/MOV
                return '.mov'
            else:
                return '.mp4'
        # Vídeo MKV (Matroska)
        elif magic_bytes[0:4] == b'\x1A\x45\xDF\xA3':
            return '.mkv'
        # Vídeo WebM / WebP / WAV (RIFF)
        elif magic_bytes[0:4] == b'RIFF':
            if magic_bytes[8:12] == b'WEBM':
                return '.webm'
            elif magic_bytes[8:12] == b'WEBP':
                return '.webp'
            elif magic_bytes[8:12] == b'WAVE':
                return '.wav'
            elif magic_bytes[8:12] == b'AVI ':
                return '.avi'
        # PNG
        elif magic_bytes[0:8] == b'\x89PNG\r\n\x1a\n':
            return '.png'
        # JPEG
        elif magic_bytes[0:3] == b'\xFF\xD8\xFF':
            return '.jpg'
        # GIF
        elif magic_bytes[0:6] in (b'GIF87a', b'GIF89a'):
            return '.gif'
        # BMP (Windows Bitmap)
        elif magic_bytes[0:2] == b'BM':
            return '.bmp'
        # MP3 (ID3 tag ou MPEG frame sync)
        elif magic_bytes[0:3] == b'ID3':
            return '.mp3'
        elif magic_bytes[0:2] == b'\xFF\xFB' or magic_bytes[0:2] == b'\xFF\xFA':
            return '.mp3'
        # OGG (Ogg Vorbis, Opus, etc)
        elif magic_bytes[0:4] == b'OggS':
            return '.ogg'
        # FLAC (Free Lossless Audio Codec)
        elif magic_bytes[0:4] == b'fLaC':
            return '.flac'
        # AAC (Advanced Audio Codec)
        elif magic_bytes[0:2] == b'\xFF\xF1' or magic_bytes[0:2] == b'\xFF\xF9':
            log.info(f"✅ Detectado: AAC (áudio)")
            return '.aac'
        # PDF
        elif magic_bytes[0:4] == b'%PDF':
            log.info(f"✅ Detectado: PDF (documento)")
            return '.pdf'
        # AVIF (modern image format)
        elif b'ftyp' in magic_bytes[:12] and b'avif' in magic_bytes[:20]:
            log.info(f"✅ Detectado: AVIF (imagem)")
            return '.avif'
        # TIFF
        elif magic_bytes[0:4] == b'II\x2A\x00' or magic_bytes[0:4] == b'MM\x00\x2A':
            log.info(f"✅ Detectado: TIFF (imagem)")
            return '.tiff'
        # SVG (XML-based, pode começar com < ou BOM)
        elif magic_bytes[0:4] == b'<?xm' or magic_bytes[0:6] == b'<svg':
            return '.svg'
    except Exception as e:
        pass  # Silencioso em caso de erro
    
    # Fallback: Se não conseguiu detectar, manter .bin
    return '.bin'




def limpar_arquivo(filename: str) -> bool:
    """Deleta arquivo da pasta uploads"""
    try:
        arquivo_path = os.path.join(UPLOADS_DIR, filename)
        if os.path.exists(arquivo_path):
            os.remove(arquivo_path)
            log.info(f"🗑️ Arquivo deletado: {filename}")
            return True
        return False
    except Exception as e:
        log.error(f"❌ Erro deletando arquivo: {e}")
        return False


def extrair_arquivo_compactado(arquivo_compactado: str, tipo_esperado: str) -> str:
    """
    Extrai arquivo compactado (ZIP, RAR, 7Z) e retorna apenas o arquivo 
    do tipo esperado (video, imagem, audio, etc)
    
    Args:
        arquivo_compactado: Caminho do arquivo .zip/.rar/.7z
        tipo_esperado: Tipo esperado (video, imagem, audio, documento, conteudo)
    
    Returns:
        Caminho do arquivo extraído ou None se falhar
    """
    import zipfile
    import tempfile
    
    # Mapeamento de tipos para extensões
    extensoes_validas = {
        'video': ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm'],
        'imagem': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'],
        'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
        'documento': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'],
        'conteudo': ['.txt', '.html', '.json', '.xml']
    }
    
    try:
        # Detectar tipo de arquivo compactado
        if not arquivo_compactado.lower().endswith(('.zip', '.rar', '.7z')):
            print(f"Arquivo compactado nao suportado: {arquivo_compactado}")
            return None
        
        # Criar temp dir para extração
        temp_dir = tempfile.mkdtemp()
        
        # Extrair ZIP (suporta ZIP nativamente)
        if arquivo_compactado.lower().endswith('.zip'):
            try:
                with zipfile.ZipFile(arquivo_compactado, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            except Exception as e:
                print(f"Erro ao descompactar ZIP: {e}")
                return None
        else:
            # Para RAR e 7Z, usar comando do sistema
            import subprocess
            if arquivo_compactado.lower().endswith('.rar'):
                cmd = ['unrar', 'x', arquivo_compactado, temp_dir]
            elif arquivo_compactado.lower().endswith('.7z'):
                cmd = ['7z', 'x', arquivo_compactado, f'-o{temp_dir}']
            
            try:
                subprocess.run(cmd, check=True, capture_output=True)
            except Exception as e:
                print(f"Erro ao descompactar arquivo: {e}")
                return None
        
        # Procurar por arquivo do tipo esperado
        extensoes = extensoes_validas.get(tipo_esperado, [])
        
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensoes):
                    arquivo_encontrado = os.path.join(root, file)
                    
                    # Copiar para pasta de uploads com nome padrão
                    output_filename = f"{tipo_esperado}_extraido_{Path(file).stem}.bin"
                    output_path = os.path.join(UPLOADS_DIR, output_filename)
                    
                    shutil.copy(arquivo_encontrado, output_path)
                    print(f"Arquivo extraido: {file} -> {output_filename}")
                    
                    # Limpar temp dir
                    shutil.rmtree(temp_dir)
                    
                    return output_path
        
        print(f"Nenhum arquivo do tipo '{tipo_esperado}' encontrado no compactado")
        shutil.rmtree(temp_dir)
        return None
        
    except Exception as e:
        print(f"Erro ao extrair arquivo compactado: {e}")
        import traceback
        traceback.print_exc()
        return None


def eh_arquivo_compactado(caminho_arquivo: str) -> bool:
    """Verifica se é um arquivo compactado"""
    return caminho_arquivo.lower().endswith(('.zip', '.rar', '.7z'))


if __name__ == "__main__":
    # Teste
    logging.basicConfig(level=logging.INFO)
    print("✅ Módulo de processamento de arquivos carregado")
