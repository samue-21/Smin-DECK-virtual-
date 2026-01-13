#!/usr/bin/env python3
"""
Sincronizador de atualizações - Busca atualizações da API
NÃO MODIFICA O ARQUIVO JSON - Apenas retorna dados para o app aplicar na memória
"""

import requests
import os
from pathlib import Path
from database_client import DatabaseClient
from database import incrementar_tentativa, obter_tentativas, deletar_atualizacao

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
        # IMPORTANTE: .bin pode ser um arquivo compactado (ZIP, RAR, 7Z) do Google Drive
        if not arquivo_path.lower().endswith(('.zip', '.rar', '.7z', '.bin')):
            return arquivo_path  # Não é compactado, retornar como está
        
        # Criar temp dir para extração
        temp_dir = tempfile.mkdtemp()
        
        # Extrair ZIP (suporta ZIP nativamente)
        # IMPORTANTE: .bin pode ser um ZIP (Google Drive)
        if arquivo_path.lower().endswith(('.zip', '.bin')):
            try:
                # Tentar com zipfile (funciona com .zip e .bin que é ZIP)
                with zipfile.ZipFile(arquivo_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            except Exception as e:
                # Se falhar como ZIP, tentar como RAR/7Z
                import subprocess
                if arquivo_path.lower().endswith('.rar'):
                    cmd = ['unrar', 'x', arquivo_path, temp_dir]
                elif arquivo_path.lower().endswith('.7z'):
                    cmd = ['7z', 'x', arquivo_path, f'-o{temp_dir}']
                else:
                    # Se for .bin mas não é ZIP válido, falhar
                    shutil.rmtree(temp_dir)
                    return None
                
                try:
                    subprocess.run(cmd, check=True, capture_output=True)
                except Exception as e:
                    shutil.rmtree(temp_dir)
                    return None
        else:
            # Para RAR e 7Z puros
            import subprocess
            if arquivo_path.lower().endswith('.rar'):
                cmd = ['unrar', 'x', arquivo_path, temp_dir]
            elif arquivo_path.lower().endswith('.7z'):
                cmd = ['7z', 'x', arquivo_path, f'-o{temp_dir}']
            else:
                # Arquivo compactado desconhecido
                shutil.rmtree(temp_dir)
                return None
            
            try:
                subprocess.run(cmd, check=True, capture_output=True)
            except Exception as e:
                shutil.rmtree(temp_dir)
                return None
        
        # Procurar por arquivo do tipo esperado
        extensoes = extensoes_validas.get(tipo_esperado, [])
        
        # Coletar TODOS os arquivos válidos encontrados
        arquivos_validos = []
        
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensoes):
                    arquivo_completo = os.path.join(root, file)
                    tamanho = os.path.getsize(arquivo_completo)
                    
                    # Calcular profundidade da pasta (raiz = 0, subpasta = 1+)
                    profundidade = root.replace(temp_dir, '').count(os.sep)
                    
                    arquivos_validos.append({
                        'path': arquivo_completo,
                        'name': file,
                        'tamanho': tamanho,
                        'profundidade': profundidade
                    })
        
        if not arquivos_validos:
            shutil.rmtree(temp_dir)
            return None
        
        # PRIORIDADE: Preferir arquivos na RAIZ, depois o MAIOR (mais provável ser o video real)
        # 1. Filtrar por profundidade (preferir raiz)
        profundidade_min = min(a['profundidade'] for a in arquivos_validos)
        arquivos_raiz = [a for a in arquivos_validos if a['profundidade'] == profundidade_min]
        
        # 2. Se tem arquivos na raiz, preferir o maior
        if arquivos_raiz:
            arquivo_selecionado = max(arquivos_raiz, key=lambda a: a['tamanho'])
        else:
            # Senao, apenas pegar o maior de todos
            arquivo_selecionado = max(arquivos_validos, key=lambda a: a['tamanho'])
        
        arquivo_encontrado = arquivo_selecionado['path']
        file = arquivo_selecionado['name']
        
        # Copiar para pasta de downloads com nome padrão (mantendo extensão original)
        output_filename = f"{tipo_esperado}_extraido_{Path(file).stem}{Path(file).suffix}"
        output_path = os.path.join(DOWNLOADS_DIR, output_filename)
        
        try:
            import shutil
            shutil.copy2(arquivo_encontrado, output_path)  # Usar copy2 para preservar metadata
        except Exception as e:
            # Se copia falhar, limpar e retornar None
            shutil.rmtree(temp_dir)
            return None
        
        # Limpar temp dir
        shutil.rmtree(temp_dir)
        
        # Deletar arquivo compactado original APENAS se copia foi bem-sucedida
        if os.path.exists(output_path):
            try:
                os.remove(arquivo_path)
            except:
                pass
            return output_path
        else:
            # Arquivo nao foi copiado, retornar None
            return None
        
    except Exception as e:
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
            return new_path
        else:
            return arquivo_path
    
    except Exception as e:
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
            
            resp = requests.get(url, timeout=30)
            
            if resp.status_code == 200:
                arquivo_path = os.path.join(DOWNLOADS_DIR, filename)
                with open(arquivo_path, 'wb') as f:
                    f.write(resp.content)
                
                # Se for compactado, extrair e filtrar por tipo
                if arquivo_path.lower().endswith(('.zip', '.rar', '.7z', '.bin')) and tipo_esperado:
                    arquivo_extraido = extrair_arquivo_compactado_cliente(arquivo_path, tipo_esperado)
                    if arquivo_extraido:
                        arquivo_path = arquivo_extraido
                    else:
                        return None
                
                # Se for .bin (que nao era arquivo compactado), converter para formato correto
                elif arquivo_path.endswith('.bin'):
                    arquivo_path = converter_bin_para_formato_correto(arquivo_path)
                
                # IMPORTANTE: Deletar arquivo do VPS após download bem-sucedido
                self.deletar_arquivo_vps(filename)
                
                return arquivo_path
            else:
                return None
        except Exception:
            return None
    
    def deletar_arquivo_vps(self, filename: str) -> bool:
        """Deleta arquivo do VPS apos consumo"""
        try:
            url = f'{API_URL}/api/arquivo/{filename}'
            resp = requests.delete(url, timeout=5)
            if resp.status_code == 200:
                return True
            return False
        except Exception:
            return False
    
    def deletar_atualizacao(self, atualizacao_id):
        """Deleta uma atualizacao da API apos processamento"""
        try:
            resp = requests.delete(f'{API_URL}/api/atualizacao/{atualizacao_id}', timeout=5)
            if resp.status_code == 200:
                return True
        except Exception:
            pass
        return False
    
    def processar_atualizacoes(self):
        """
        Processa atualizacoes e retorna lista de mudancas para aplicar na memoria.
        NAO MODIFICA ARQUIVO - retorna dados para o DeckWindow aplicar.
        
        Sistema de 2 tentativas:
        - 1ª falha: Incrementa contador e tenta novamente na proxima sincronizacao
        - 2ª falha: Marca para limpeza automática (chama limpar_atualizacoes_falhadas.py)
        
        OTIMIZACAO: Logs MINIMOS - so mostra sucessos!
        
        Returns:
            list: Lista de dicts com mudancas para aplicar
        """
        atualizacoes = self.buscar_atualizacoes()
        
        # SILENCIADO: Se nao tem atualizacoes, NAO logar nada (evita spam)
        if not atualizacoes:
            return None
        
        mudancas = []
        
        for atualiza in atualizacoes:
            atualizacao_id = atualiza.get('id')
            botao_num = atualiza['botao']
            
            # O bot agora manda indices 0-11 diretamente
            if botao_num > 11:
                botao_idx = botao_num - 1  # 12 -> 11
            else:
                botao_idx = botao_num  # Ja esta 0-11, usar direto
            
            tipo = atualiza['tipo']  # 'link', 'video', 'imagem', 'conteudo'
            dados = atualiza['dados']  # Estrutura: {'arquivo': 'video_botao_7.bin', 'nome': 'primicias-de-fe'} OU {'conteudo': '...'}
            
            # ============================================
            # VERIFICAR NÚMERO DE TENTATIVAS
            # ============================================
            tentativas_atuais = obter_tentativas(atualizacao_id) if atualizacao_id else 0
            
            if tentativas_atuais >= 2:
                # ERRO SILENCIOSO: Limpar automaticamente sem logar
                self._agendar_limpeza(atualizacao_id, tipo, dados)
                deletar_atualizacao(atualizacao_id)
                continue
            
            # Suportar ambos os formatos antigos e novos
            if 'arquivo' in dados:
                arquivo_para_download = dados['arquivo']
                nome_botao = dados.get('nome', arquivo_para_download)
            else:
                # Formato antigo
                arquivo_para_download = dados.get('conteudo', '')
                nome_botao = arquivo_para_download
            
            # Se for arquivo, fazer download
            arquivo_local_path = os.path.join(DOWNLOADS_DIR, arquivo_para_download)
            if tipo in ('video', 'imagem') and os.path.exists(arquivo_local_path):
                # Arquivo ja foi baixado - SUCESSO SILENCIOSO
                arquivo_local = arquivo_local_path
            elif tipo in ('video', 'imagem'):
                # Fazer download do arquivo
                arquivo_local = self.baixar_arquivo(arquivo_para_download, tipo)
                if not arquivo_local:
                    # FALHA SILENCIOSA: Incrementar tentativa e continuar
                    nova_tentativa = incrementar_tentativa(atualizacao_id) if atualizacao_id else 0
                    
                    if nova_tentativa >= 2:
                        # Atingiu limite - agendar limpeza silenciosamente
                        self._agendar_limpeza(atualizacao_id, tipo, dados)
                        deletar_atualizacao(atualizacao_id)
                    # Pular para proxima atualização (retry na proxima sincronizacao)
                    continue
            else:
                arquivo_local = arquivo_para_download
            
            # Criar mudanca para aplicar na memoria
            mudanca = {
                'botao_idx': botao_idx,
                'file': arquivo_local,
                'is_youtube': 'youtube.com' in arquivo_para_download or 'youtu.be' in arquivo_para_download,
                'tipo': tipo,
                'atualizacao_id': atualizacao_id,
                'nome_arquivo': arquivo_para_download if tipo in ('video', 'imagem') else None,
                'nome_botao': nome_botao
            }
            mudancas.append(mudanca)
            
            # SUCESSO: Deletar da API apos processamento
            if atualizacao_id:
                sucesso = self.deletar_atualizacao(atualizacao_id)
                # SILENCIOSO: Nao logar deletar da fila
        
        return mudancas if mudancas else None
    
    def _agendar_limpeza(self, atualizacao_id, tipo, dados):
        """Agenda limpeza de atualizacoes falhadas (SILENCIOSO - sem logs)"""
        try:
            import subprocess
            script_path = os.path.join(os.path.dirname(__file__), 'limpar_atualizacoes_falhadas.py')
            
            # Executar script de limpeza em background (STDERR redirecionado para silenciar)
            subprocess.Popen([
                'python', script_path,
                '--atualizacao_id', str(atualizacao_id),
                '--tipo', str(tipo)
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            # Silencioso: erro ao agendar, ignorar
            pass


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
