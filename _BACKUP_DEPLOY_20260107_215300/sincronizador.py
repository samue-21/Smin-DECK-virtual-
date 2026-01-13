#!/usr/bin/env python3
"""
Sincronizador de atualizações - Busca atualizações da API
NÃO MODIFICA O ARQUIVO JSON - Apenas retorna dados para o app aplicar na memória
"""

import requests
import os
from pathlib import Path
from database_client import DatabaseClient

API_URL = 'http://72.60.244.240:5001'
DOWNLOADS_DIR = os.path.expanduser('~/.smindeckbot/downloads')

# Garantir que pasta de downloads existe
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

def extrair_arquivo_compactado_cliente(arquivo_path: str, tipo_esperado: str) -> str:
    """
    Extrai arquivo compactado (ZIP, RAR, 7Z) no cliente e retorna apenas 
    o arquivo do tipo esperado
    
    Args:
        arquivo_path: Caminho do arquivo .zip/.rar/.7z baixado
        tipo_esperado: Tipo esperado (video, imagem, audio, documento, conteudo)
    
    Returns:
        Caminho do arquivo extraído ou None se falhar
    """
    import zipfile
    import tempfile
    import shutil
    
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
        if not arquivo_path.lower().endswith(('.zip', '.rar', '.7z')):
            return arquivo_path  # Não é compactado, retornar como está
        
        print(f"[CLIENTE] Detectado arquivo compactado: {os.path.basename(arquivo_path)}")
        
        # Criar temp dir para extração
        temp_dir = tempfile.mkdtemp()
        
        # Extrair ZIP (suporta ZIP nativamente)
        if arquivo_path.lower().endswith('.zip'):
            try:
                with zipfile.ZipFile(arquivo_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            except Exception as e:
                print(f"[ERRO] Erro ao descompactar ZIP: {e}")
                shutil.rmtree(temp_dir)
                return None
        else:
            # Para RAR e 7Z, usar comando do sistema
            import subprocess
            if arquivo_path.lower().endswith('.rar'):
                cmd = ['unrar', 'x', arquivo_path, temp_dir]
            elif arquivo_path.lower().endswith('.7z'):
                cmd = ['7z', 'x', arquivo_path, f'-o{temp_dir}']
            
            try:
                subprocess.run(cmd, check=True, capture_output=True)
            except Exception as e:
                print(f"[ERRO] Erro ao descompactar arquivo: {e}")
                shutil.rmtree(temp_dir)
                return None
        
        # Procurar por arquivo do tipo esperado
        extensoes = extensoes_validas.get(tipo_esperado, [])
        
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensoes):
                    arquivo_encontrado = os.path.join(root, file)
                    
                    # Copiar para pasta de downloads com nome padrão
                    output_filename = f"{tipo_esperado}_extraido_{Path(file).stem}.bin"
                    output_path = os.path.join(DOWNLOADS_DIR, output_filename)
                    
                    import shutil
                    shutil.copy(arquivo_encontrado, output_path)
                    print(f"[CLIENTE] Arquivo extraido: {file} -> {output_filename}")
                    
                    # Limpar temp dir
                    shutil.rmtree(temp_dir)
                    
                    # Deletar arquivo compactado original
                    try:
                        os.remove(arquivo_path)
                        print(f"[CLIENTE] Arquivo compactado removido: {os.path.basename(arquivo_path)}")
                    except:
                        pass
                    
                    return output_path
        
        print(f"[AVISO] Nenhum arquivo do tipo '{tipo_esperado}' encontrado no compactado")
        shutil.rmtree(temp_dir)
        return None
        
    except Exception as e:
        print(f"[ERRO] Erro ao extrair arquivo compactado: {e}")
        import traceback
        traceback.print_exc()
        return None

def converter_bin_para_formato_correto(arquivo_path: str) -> str:
    """
    Detecta o tipo real de um arquivo .bin e o converte para extensão correta
    Usa magic bytes para identificar o tipo
    
    Returns:
        Caminho do arquivo convertido ou original se não conseguir detectar
    """
    if not arquivo_path.endswith('.bin'):
        return arquivo_path
    
    if not os.path.exists(arquivo_path):
        return arquivo_path
    
    try:
        # Ler primeiros bytes para detectar tipo
        with open(arquivo_path, 'rb') as f:
            magic_bytes = f.read(32)
        
        # Detectar tipo por magic bytes
        new_ext = None
        
        # Vídeo MP4
        if magic_bytes[4:8] == b'ftyp':
            new_ext = '.mp4'
        # Vídeo MKV
        elif magic_bytes[0:4] == b'\x1A\x45\xDF\xA3':
            new_ext = '.mkv'
        # Vídeo WebM
        elif magic_bytes[0:4] == b'\x1A\x45\xDF\xA3':
            new_ext = '.webm'
        # PNG
        elif magic_bytes[0:8] == b'\x89PNG\r\n\x1a\n':
            new_ext = '.png'
        # JPEG
        elif magic_bytes[0:3] == b'\xFF\xD8\xFF':
            new_ext = '.jpg'
        # GIF
        elif magic_bytes[0:6] in (b'GIF87a', b'GIF89a'):
            new_ext = '.gif'
        # BMP
        elif magic_bytes[0:2] == b'BM':
            new_ext = '.bmp'
        # WebP
        elif magic_bytes[0:4] == b'RIFF' and magic_bytes[8:12] == b'WEBP':
            new_ext = '.webp'
        # MP3
        elif magic_bytes[0:3] == b'ID3' or magic_bytes[0:2] == b'\xFF\xFB':
            new_ext = '.mp3'
        # WAV
        elif magic_bytes[0:4] == b'RIFF' and magic_bytes[8:12] == b'WAVE':
            new_ext = '.wav'
        # OGG
        elif magic_bytes[0:4] == b'OggS':
            new_ext = '.ogg'
        
        if new_ext:
            new_path = arquivo_path[:-4] + new_ext  # Remove .bin e adiciona extensão correta
            os.rename(arquivo_path, new_path)
            print(f"🔄 Arquivo convertido: {os.path.basename(arquivo_path)} → {os.path.basename(new_path)}")
            return new_path
        else:
            print(f"⚠️  Tipo do arquivo não reconhecido, mantendo .bin")
            return arquivo_path
    
    except Exception as e:
        print(f"⚠️  Erro ao converter .bin: {e}")
        return arquivo_path

class AtualizadorDeck:
    def __init__(self):
        self.db_client = DatabaseClient()
    
    def buscar_atualizacoes(self):
        """Busca atualizações da API"""
        try:
            resp = requests.get(f'{API_URL}/api/atualizacoes', timeout=10)
            if resp.status_code == 200:
                return resp.json().get('atualizacoes', [])
        except Exception as e:
            print(f"❌ Erro ao buscar atualizações: {e}")
        return []
    
    def baixar_arquivo(self, filename: str, tipo_esperado: str = None) -> str:
        """
        Baixa arquivo do servidor e extrai se for compactado
        
        Args:
            filename: Nome do arquivo para download
            tipo_esperado: Tipo esperado (video, imagem, etc) - usado para filtrar arquivos compactados
        
        Returns:
            Caminho do arquivo baixado/extraído ou None se falhar
        """
        try:
            url = f'{API_URL}/api/arquivo/{filename}'
            print(f"[CLIENTE] Tentando download: {url}")
            
            resp = requests.get(url, timeout=30)
            print(f"[CLIENTE] Status da resposta: {resp.status_code}")
            
            if resp.status_code == 200:
                arquivo_path = os.path.join(DOWNLOADS_DIR, filename)
                with open(arquivo_path, 'wb') as f:
                    f.write(resp.content)
                print(f"[OK] Arquivo salvo: {arquivo_path} ({len(resp.content) / 1024:.1f}KB)")
                
                # Se for compactado, extrair e filtrar por tipo
                if arquivo_path.lower().endswith(('.zip', '.rar', '.7z')) and tipo_esperado:
                    print(f"[CLIENTE] Extraindo e filtrando arquivo compactado para tipo '{tipo_esperado}'...")
                    arquivo_extraido = extrair_arquivo_compactado_cliente(arquivo_path, tipo_esperado)
                    if arquivo_extraido:
                        print(f"[OK] Arquivo extraído e filtrado: {arquivo_extraido}")
                        arquivo_path = arquivo_extraido
                    else:
                        print(f"[AVISO] Falha ao extrair - usando arquivo original se possível")
                        # Manter arquivo original se extração falhar
                
                # Se for .bin, converter para formato correto
                elif arquivo_path.endswith('.bin'):
                    print(f"[CLIENTE] Convertendo .bin para formato correto...")
                    arquivo_path = converter_bin_para_formato_correto(arquivo_path)
                
                # IMPORTANTE: Deletar arquivo do VPS após download bem-sucedido
                print(f"[CLIENTE] Deletando arquivo do VPS...")
                self.deletar_arquivo_vps(filename)
                
                return arquivo_path
            else:
                print(f"[ERRO] HTTP {resp.status_code} ao baixar {filename}")
                print(f"       Resposta: {resp.text[:200]}")
                return None
        except Exception as e:
            print(f"[ERRO] Erro ao baixar arquivo: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def deletar_arquivo_vps(self, filename: str) -> bool:
        """Deleta arquivo do VPS após consumo"""
        try:
            url = f'{API_URL}/api/arquivo/{filename}'
            resp = requests.delete(url, timeout=5)
            if resp.status_code == 200:
                print(f"🗑️  Arquivo {filename} deletado do VPS")
                return True
            return False
        except Exception as e:
            print(f"⚠️  Erro ao deletar arquivo: {e}")
            return False
    
    def deletar_atualizacao(self, atualizacao_id):
        """Deleta uma atualização da API após processamento"""
        try:
            resp = requests.delete(f'{API_URL}/api/atualizacao/{atualizacao_id}', timeout=5)
            if resp.status_code == 200:
                print(f"🗑️  Atualização {atualizacao_id} removida da fila")
                return True
            else:
                print(f"⚠️  Falha ao remover atualização {atualizacao_id}")
        except Exception as e:
            print(f"⚠️  Erro ao deletar atualização {atualizacao_id}: {e}")
        return False
    
    def processar_atualizacoes(self):
        """
        Processa atualizações e retorna lista de mudanças para aplicar na memória.
        NÃO MODIFICA ARQUIVO - retorna dados para o DeckWindow aplicar.
        
        Returns:
            list: Lista de dicts com mudanças para aplicar
        """
        atualizacoes = self.buscar_atualizacoes()
        print(f"🔍 DEBUG: Buscando atualizações... Encontradas: {len(atualizacoes) if atualizacoes else 0}")
        if not atualizacoes:
            print(f"ℹ️ Nenhuma atualização na fila")
            return None
        
        mudancas = []
        
        for atualiza in atualizacoes:
            atualizacao_id = atualiza.get('id')
            botao_num = atualiza['botao']
            
            # O bot agora manda índices 0-11 diretamente
            # Só converter se for > 11 (registro antigo no formato 1-12)
            if botao_num > 11:
                botao_idx = botao_num - 1  # 12 -> 11
                print(f"⚙️  Convertendo índice antigo: {botao_num} -> {botao_idx}")
            else:
                botao_idx = botao_num  # Já está 0-11, usar direto
            
            tipo = atualiza['tipo']  # 'link', 'video', 'imagem', 'conteudo'
            dados = atualiza['dados']  # Estrutura: {'arquivo': 'video_botao_7.bin', 'nome': 'primicias-de-fe'} OU {'conteudo': '...'}
            
            # Suportar ambos os formatos antigos e novos
            # Novo formato (com arquivo + nome):
            if 'arquivo' in dados:
                arquivo_para_download = dados['arquivo']  # Nome real do arquivo (video_botao_7.bin)
                nome_botao = dados.get('nome', arquivo_para_download)  # Nome customizado para exibição
            else:
                # Formato antigo (conteúdo direto):
                arquivo_para_download = dados.get('conteudo', '')
                nome_botao = arquivo_para_download
            
            print(f"📝 Atualização Botão {botao_idx+1} (índice {botao_idx}): {tipo}")
            print(f"   🔹 Arquivo: {arquivo_para_download}")
            print(f"   🔹 Nome botão: {nome_botao}")
            
            # Se for arquivo, fazer download
            arquivo_local_path = os.path.join(DOWNLOADS_DIR, arquivo_para_download)
            if tipo in ('video', 'imagem') and os.path.exists(arquivo_local_path):
                # Arquivo já foi baixado
                print(f"✅ Arquivo já existe localmente: {arquivo_local_path}")
                arquivo_local = arquivo_local_path
            elif tipo in ('video', 'imagem'):
                # Fazer download do arquivo (usando nome real do arquivo)
                print(f"[CLIENTE] Baixando arquivo do VPS: {arquivo_para_download}")
                arquivo_local = self.baixar_arquivo(arquivo_para_download, tipo)
                if not arquivo_local:
                    print(f"[ERRO] Arquivo não foi baixado, pulando atualização")
                    continue
                print(f"[OK] Download concluído: {arquivo_local}")
            else:
                arquivo_local = arquivo_para_download
            
            # Criar mudança para aplicar na memória
            mudanca = {
                'botao_idx': botao_idx,
                'file': arquivo_local,
                'is_youtube': 'youtube.com' in arquivo_para_download or 'youtu.be' in arquivo_para_download,
                'tipo': tipo,
                'atualizacao_id': atualizacao_id,
                'nome_arquivo': arquivo_para_download if tipo in ('video', 'imagem') else None,
                'nome_botao': nome_botao  # ⭐ NOVO: Nome customizado para exibir no botão
            }
            mudancas.append(mudanca)
            
            # Deletar da API imediatamente após processar
            if atualizacao_id:
                self.deletar_atualizacao(atualizacao_id)
        
        return mudancas if mudancas else None


# Para testes manuais
if __name__ == '__main__':
    atualizador = AtualizadorDeck()
    mudancas = atualizador.processar_atualizacoes()
    if mudancas:
        print(f"\n✅ {len(mudancas)} mudanças para aplicar:")
        for m in mudancas:
            print(f"   Botão {m['botao_idx']}: {m['file'][:50]}...")
    else:
        print("ℹ️ Nenhuma atualização pendente")
