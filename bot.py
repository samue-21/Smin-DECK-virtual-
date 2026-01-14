#!/usr/bin/env python3
"""
🤖 SminDeck Bot - Assistente Virtual com Menu de Botões
Fluxo: Chave → 4 Opções Principais → 12 Botões para Atualizar → Executa
Usando banco de dados SQLite centralizado
"""

import discord
from discord.ext import commands, tasks
from discord import app_commands, ui
import os
import sys
import random
import string
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta
import asyncio
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from urllib.parse import urlparse
from database import init_database, criar_chave, validar_chave, obter_info_chave, registrar_atualizacao, usuario_esta_ativo
import logging
import aiohttp  # Para fazer download assíncrono
from download_manager import download_arquivo, validar_extensao as validar_ext_url
import re  # Para detectar URLs

# Setup logging
_LOG_FILE = '/opt/smindeck-bot/debug.log'
if os.name == 'nt':
    _LOG_FILE = 'bot_debug.log'
else:
    try:
        os.makedirs(os.path.dirname(_LOG_FILE), exist_ok=True)
    except Exception:
        # Se não conseguir criar /opt, cai para log local
        _LOG_FILE = 'bot_debug.log'

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)-8s] %(message)s',
    handlers=[
        logging.FileHandler(_LOG_FILE),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    log.error("DISCORD_TOKEN não encontrado")
    sys.exit(1)

intents = discord.Intents(guilds=True, guild_messages=True, message_content=True, members=False)
bot = commands.Bot(command_prefix='/', intents=intents)

# ============================================================
# ARMAZENAMENTO
# ============================================================

CHAVES_ATIVAS = {}
USUARIOS_AUTENTICADOS = {}
CONTEXTO_USUARIO = {}  # {user_id: {'opcao': '1', 'botao': None, 'dados': {}, 'timestamp': time.time()}}

# Armazenar referências para enviar mensagens
USER_CHANNELS = {}  # {user_id: channel_id}

# Arquivo para persistir usuários autenticados entre APP e Bot
import os
import time
AUTHENTICATED_FILE = os.path.expanduser('~/.smindeckbot/authenticated.json')

# ✅ TIMEOUT para contextos expirados (5 minutos)
CONTEXT_TIMEOUT = 300

# ============================================================
# SERVIDOR HTTP (HTTP Server nativo Python)
# ============================================================

class AuthHandler(BaseHTTPRequestHandler):
    """Handler para requisições HTTP de autenticação"""
    
    def do_POST(self):
        """Processa POST requests"""
        if self.path == '/auth_webhook':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                data = json.loads(body)
                
                user_id = data.get('user_id')
                guild_id = data.get('guild_id')
                channel_id = data.get('channel_id')
                
                if user_id and guild_id and channel_id:
                    # Notificar no loop do bot
                    asyncio.run_coroutine_threadsafe(
                        notificar_autenticacao(user_id, guild_id, channel_id),
                        bot.loop
                    )
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'ok'}).encode())
                else:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Missing data'}).encode())
            except Exception as e:
                print(f"❌ Erro no webhook: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        """Processa GET requests"""
        if self.path.startswith('/key_info/'):
            try:
                chave = self.path.split('/key_info/')[1].upper()
                
                if chave in CHAVES_ATIVAS:
                    info = CHAVES_ATIVAS[chave]
                    data = {
                        'user_id': info['user_id'],
                        'guild_id': info['guild_id'],
                        'channel_id': info.get('channel_id', 0),
                        'valid': True
                    }
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(data).encode())
                else:
                    self.send_response(404)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'valid': False}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Silencia logs padrão do servidor HTTP"""
        pass

def start_web_server():
    """Inicia servidor HTTP em thread separada"""
    try:
        server = HTTPServer(('0.0.0.0', 5000), AuthHandler)
        server.serve_forever()
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor HTTP: {e}")# ============================================================
# VIEWS COM BOTÕES
# ============================================================

class MenuPrincipal(ui.View):
    """Menu principal com 4 opções"""
    
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
    
    @ui.button(label="🔗 Atualizar Link", style=discord.ButtonStyle.primary)
    async def link(self, interaction: discord.Interaction, button: ui.Button):
        await self.callback(interaction, "link")
    
    @ui.button(label="🎥 Atualizar Vídeo", style=discord.ButtonStyle.primary)
    async def video(self, interaction: discord.Interaction, button: ui.Button):
        await self.callback(interaction, "video")
    
    @ui.button(label="🖼️ Atualizar Imagem", style=discord.ButtonStyle.primary)
    async def imagem(self, interaction: discord.Interaction, button: ui.Button):
        await self.callback(interaction, "imagem")
    
    @ui.button(label="📁 Enviar Arquivos", style=discord.ButtonStyle.primary)
    async def conteudo(self, interaction: discord.Interaction, button: ui.Button):
        await self.callback(interaction, "conteudo")

class Menu12Botoes(ui.View):
    """Menu com 12 botões para escolher qual atualizar"""
    
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
    
    @ui.button(label="Botão 1", style=discord.ButtonStyle.primary)
    async def btn1(self, interaction: discord.Interaction, button: ui.Button):
        await self.callback(interaction, "0")
    
    @ui.button(label="Botão 2", style=discord.ButtonStyle.primary)
    async def btn2(self, interaction: discord.Interaction, button: ui.Button):
        await self.callback(interaction, "1")
    
    @ui.button(label="Botão 3", style=discord.ButtonStyle.primary)
    async def btn3(self, interaction: discord.Interaction, button: ui.Button):
        await self.callback(interaction, "2")
    
    @ui.button(label="Botão 4", style=discord.ButtonStyle.primary)
    async def btn4(self, interaction: discord.Interaction, button: ui.Button):
        await self.callback(interaction, "3")
    
    @ui.button(label="Botão 5", style=discord.ButtonStyle.primary)
    async def btn5(self, interaction: discord.Interaction, button: ui.Button):
        await self.callback(interaction, "4")
    
    @ui.button(label="Botão 6", style=discord.ButtonStyle.primary)
    async def btn6(self, interaction: discord.Interaction, button: ui.Button):
        await self.callback(interaction, "5")
    
    @ui.button(label="Botão 7", style=discord.ButtonStyle.primary)
    async def btn7(self, interaction: discord.Interaction, button: ui.Button):
        await self.callback(interaction, "6")
    
    @ui.button(label="Botão 8", style=discord.ButtonStyle.primary)
    async def btn8(self, interaction: discord.Interaction, button: ui.Button):
        await self.callback(interaction, "7")

class Menu12Botoes2(ui.View):
    """Menu com botões 9-12"""
    
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
    
    @ui.button(label="Botão 9", style=discord.ButtonStyle.primary)
    async def btn9(self, interaction: discord.Interaction, button: ui.Button):
        await self.callback(interaction, "8")
    
    @ui.button(label="Botão 10", style=discord.ButtonStyle.primary)
    async def btn10(self, interaction: discord.Interaction, button: ui.Button):
        await self.callback(interaction, "9")
    
    @ui.button(label="Botão 11", style=discord.ButtonStyle.primary)
    async def btn11(self, interaction: discord.Interaction, button: ui.Button):
        await self.callback(interaction, "10")
    
    @ui.button(label="Botão 12", style=discord.ButtonStyle.primary)
    async def btn12(self, interaction: discord.Interaction, button: ui.Button):
        await self.callback(interaction, "11")

# ============================================================
# FUNÇÕES
# ============================================================

def gerar_chave():
    """Gera nova chave e salva no banco de dados"""
    try:
        chave = criar_chave(user_id=0, guild_id=0, channel_id=0)
        log.info(f"🔑 Chave gerada: {chave}")
        print(f"🔑 Chave gerada: {chave}")
        if chave is None:
            log.warning(f"⚠️ AVISO: criar_chave() retornou None!")
            print(f"⚠️ AVISO: criar_chave() retornou None!")
        return chave
    except Exception as e:
        log.error(f"❌ Erro em gerar_chave: {e}")
        print(f"❌ Erro em gerar_chave: {e}")
        import traceback
        traceback.print_exc()
        return None

def check_validar_chave(chave, user_id, guild_id, channel_id):
    """Valida chave usando banco de dados"""
    sucesso, msg = validar_chave(chave, user_id, guild_id, channel_id)
    return sucesso, msg

def usuario_autenticado(user_id):
    """Verifica se usuário está autenticado - checa memória primeiro, depois banco"""
    try:
        # Verificar em memória primeiro (usuarios carregados no startup)
        if user_id in USUARIOS_AUTENTICADOS:
            return True
        
        # Verificar no banco de dados
        result = usuario_esta_ativo(user_id)
        
        # Se está ativo no banco, carregar em memória
        if result:
            USUARIOS_AUTENTICADOS[user_id] = {'autenticado': True}
        
        log.info(f"usuario_autenticado({user_id}) = {result}")
        return result
    except Exception as e:
        log.error(f"Erro ao verificar autenticação: {e}")
        return False

def marcar_autenticado(user_id, guild_id, channel_id):
    """Marca usuário como autenticado e salva em arquivo"""
    # Em memória
    USUARIOS_AUTENTICADOS[user_id] = {
        'guild_id': guild_id,
        'autenticado_em': datetime.now().isoformat(),
        'channel_id': channel_id
    }
    USER_CHANNELS[user_id] = channel_id
    
    # Em arquivo
    try:
        os.makedirs(os.path.dirname(AUTHENTICATED_FILE), exist_ok=True)
        data = {}
        if os.path.exists(AUTHENTICATED_FILE):
            with open(AUTHENTICATED_FILE, 'r') as f:
                data = json.load(f)
        
        data[str(user_id)] = {
            'guild_id': guild_id,
            'channel_id': channel_id,
            'autenticado_em': datetime.now().isoformat()
        }
        
        with open(AUTHENTICATED_FILE, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(f"⚠️ Erro ao salvar autenticação: {e}")

async def continuar_processamento_url(arquivo_path, opcao, botao, user_id, nome_final, tipos_permitidos, msg):
    """Continua processamento após usuário escolher nome"""
    from arquivo_processor import processar_arquivo
    from database import listar_chaves_ativas
    
    if not arquivo_path:
        await msg.edit(embed=discord.Embed(
            title="❌ ERRO NO DOWNLOAD",
            description="Não foi possível fazer download",
            color=discord.Color.red()
        ))
        return
    
    # Validar extensão
    ext = os.path.splitext(arquivo_path)[1].lower()
    if opcao not in tipos_permitidos or ext not in tipos_permitidos.get(opcao, []):
        try:
            os.remove(arquivo_path)
        except:
            pass
        await msg.edit(embed=discord.Embed(
            title="❌ TIPO NÃO PERMITIDO",
            description=f"Para {opcao}: {', '.join(tipos_permitidos[opcao])}",
            color=discord.Color.red()
        ))
        return
    
    # Processar
    embed_proc = discord.Embed(
        title="⚙️ PROCESSANDO",
        description="Otimizando arquivo...",
        color=discord.Color.blue()
    )
    await msg.edit(embed=embed_proc)
    
    # Usar nome padronizado para o arquivo (tipo_botao_X)
    # Exemplo: video_botao_7, imagem_botao_3
    tipo_padrao = {'video': 'video', 'imagem': 'imagem', 'link': 'link'}
    prefixo = tipo_padrao.get(opcao, 'arquivo')
    arquivo_padrao = f"{prefixo}_botao_{botao}"
    
    print(f"⚙️ Processando arquivo: {arquivo_path} → {arquivo_padrao}")
    
    # Modificar arquivo_processor para usar nome padronizado
    # Mas primeiro, vamos usar o processamento normal
    arquivo_processado = processar_arquivo(arquivo_path, opcao, botao)
    
    try:
        os.remove(arquivo_path)
    except:
        pass
    
    if not arquivo_processado:
        # DEBUG: Se processar_arquivo falhou, tenta copiar arquivo bruto como fallback
        print(f"⚠️ Erro ao processar arquivo, tentando fallback...")
        tipo_padrao = {'video': 'video', 'imagem': 'imagem', 'link': 'link'}
        prefixo = tipo_padrao.get(opcao, 'arquivo')
        
        # Detectar extensão
        ext = os.path.splitext(arquivo_path)[1].lower() or '.bin'
        nome_fallback = f"{prefixo}_botao_{botao}{ext}"
        path_fallback = os.path.join('/opt/smindeck-bot/uploads' if os.name != 'nt' else 'uploads', nome_fallback)
        
        try:
            import shutil
            shutil.copy(arquivo_path, path_fallback)
            arquivo_processado = path_fallback
            print(f"✅ Fallback: arquivo copiado como {nome_fallback}")
        except Exception as e:
            print(f"❌ Fallback também falhou: {e}")
            await msg.edit(embed=discord.Embed(
                title="❌ ERRO",
                description="Erro ao processar arquivo",
                color=discord.Color.red()
            ))
            return
    
    # Registrar no banco
    chaves = listar_chaves_ativas()
    chave_usuario = None
    for c in chaves:
        if c['user_id'] == user_id:
            chave_usuario = c['chave']
            break
    
    if chave_usuario:
        # Arquivo real no VPS (para download): nome padronizado
        nome_arquivo_real = os.path.basename(arquivo_processado)
        
        # Registrar no banco com DOIS DADOS:
        # 1. arquivo: nome real para download (video_botao_7.bin)
        # 2. nome: nome customizado para exibir no botão (01-10-26_%20primicias-de-fe)
        dados_registro = {
            'arquivo': nome_arquivo_real,  # Nome real do arquivo no VPS
            'nome': nome_final              # Nome customizado para exibição
        }
        registrar_atualizacao(chave_usuario, opcao, botao, dados_registro)
        
        print(f"✅ Arquivo registrado: {nome_arquivo_real}")
        print(f"   📁 Exibição no botão: {nome_final}")
        log.info(f"✅ Arquivo registrado: {nome_arquivo_real} (exibir como: {nome_final})")
    
    tamanho = os.path.getsize(arquivo_processado) / (1024 * 1024)
    embed_final = discord.Embed(
        title="✅ ATUALIZADO!",
        description=f"**Botão {botao + 1}**\n📁 {nome_final}\n📊 {tamanho:.1f}MB\n✨ Sincronizado!\n\n💡 *Se você já tinha enviado outro arquivo para este botão, o anterior foi descartado automaticamente.*",
        color=discord.Color.green()
    )
    await msg.edit(embed=embed_final)
    
    # LIMPEZA DO CANAL: Deletar mensagens antigas, manter apenas a última
    try:
        await limpar_canal_manter_ultima(msg.channel)
    except Exception as e:
        print(f"⚠️ Erro ao limpar canal: {e}")

async def limpar_canal_manter_ultima(channel):
    """
    Limpa o canal: deleta todas as mensagens do bot MENOS a última.
    Mantém o canal limpo e organizado!
    """
    try:
        mensagens_para_deletar = []
        ultima_mensagem = None
        
        # Buscar últimas 50 mensagens para encontrar mensagens do bot
        async for mensagem in channel.history(limit=50):
            if mensagem.author == bot.user:
                if ultima_mensagem is None:
                    # A primeira (mais recente) é a última
                    ultima_mensagem = mensagem
                else:
                    # Outras mensagens antigas do bot devem ser deletadas
                    mensagens_para_deletar.append(mensagem)
        
        # Deletar as mensagens antigas (máximo 100 por vez)
        if mensagens_para_deletar:
            print(f"🧹 Limpando {len(mensagens_para_deletar)} mensagens antigas do canal...")
            for msg_antiga in mensagens_para_deletar[:100]:  # Limit de 100
                try:
                    await msg_antiga.delete()
                except Exception as e:
                    print(f"⚠️ Erro ao deletar mensagem: {e}")
            
            if len(mensagens_para_deletar) > 0:
                print(f"✅ Canal limpo! Mantida apenas a última mensagem.")
    except Exception as e:
        print(f"⚠️ Erro na limpeza do canal: {e}")

async def notificar_autenticacao(user_id, guild_id, channel_id):
    """Chamado pelo APP quando autentica uma chave"""
    marcar_autenticado(user_id, guild_id, channel_id)
    
    try:
        guild = bot.get_guild(guild_id)
        if guild:
            channel = guild.get_channel(channel_id)
            if channel:
                # Boas-vindas
                embed = discord.Embed(
                    title="🎉 BEM-VINDO!",
                    description="Sua autenticação foi confirmada!\n\nAgora você tem acesso completo. ✨",
                    color=discord.Color.green()
                )
                await channel.send(embed=embed)
    except Exception as e:
        print(f"❌ Erro ao notificar autenticação: {e}")

async def mostrar_menu_principal(channel):
    """Mostra o menu com 4 opções principais"""
    try:
        if channel is None:
            log.error("Canal é None em mostrar_menu_principal")
            return
            
        embed = discord.Embed(
            title="🎯 O QUE VOCÊ PRECISA?",
            description="Escolha uma opção abaixo e vou te ajudar com alegria! 😊",
            color=discord.Color.gold()
        )
        embed.add_field(name="🔗 Atualizar Link", value="Adicione ou mude um link", inline=False)
        embed.add_field(name="🎥 Atualizar Vídeo", value="Adicione ou mude um vídeo", inline=False)
        embed.add_field(name="🖼️ Atualizar Imagem", value="Adicione ou mude uma imagem", inline=False)
        embed.add_field(name="📁 Enviar Arquivos", value="Ver e gerenciar tudo", inline=False)
        embed.set_footer(text="✨ Clique em qualquer botão!")
        
        view = MenuPrincipal(processar_opcao_principal)
        await channel.send(embed=embed, view=view)
        log.debug(f"Menu principal enviado para {channel}")
    except Exception as e:
        log.error(f"Erro em mostrar_menu_principal: {e}", exc_info=True)

async def mostrar_menu_12botoes(channel):
    """Mostra o menu com 12 botões para escolher qual atualizar"""
    embed = discord.Embed(
        title="📍 EM QUAL BOTÃO VOCÊ DESEJA ATUALIZAR?",
        description="Escolha o botão que deseja modificar:",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Clique no botão desejado!")
    
    view1 = Menu12Botoes(processar_escolha_botao)
    view2 = Menu12Botoes2(processar_escolha_botao)
    
    await channel.send(embed=embed)
    await channel.send("", view=view1)
    await channel.send("", view=view2)

async def processar_opcao_principal(interaction: discord.Interaction, opcao: str):
    """Processa a escolha do menu principal"""
    try:
        await interaction.response.defer()  # Reconhece a interação imediatamente
        
        user_id = interaction.user.id
        
        # 📝 Armazenar contexto com timestamp
        CONTEXTO_USUARIO[user_id] = {
            'opcao': opcao, 
            'botao': None, 
            'dados': {},
            'timestamp': time.time()  # ⏰ Marca quando foi criado
        }
        
        opcoes = {
            "link": "🔗 Atualizar Link",
            "video": "🎥 Atualizar Vídeo",
            "imagem": "🖼️ Atualizar Imagem",
            "conteudo": "📁 Enviar Arquivos"
        }
        
        embed = discord.Embed(
            title=opcoes.get(opcao, "Opção"),
            description="Em qual botão você deseja atualizar?",
            color=discord.Color.blue()
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        
        # Mostrar menu com 12 botões
        await mostrar_menu_12botoes(interaction.channel)
    except Exception as e:
        log.error(f"Erro em processar_opcao_principal: {e}", exc_info=True)
        try:
            await interaction.response.send_message(f"❌ Erro: {str(e)}", ephemeral=True)
        except:
            pass

async def processar_escolha_botao(interaction: discord.Interaction, botao: str):
    """Processa qual botão foi escolhido"""
    try:
        await interaction.response.defer()  # Reconhece a interação
        
        user_id = interaction.user.id
        
        if user_id not in CONTEXTO_USUARIO:
            await interaction.followup.send("❌ Contexto perdido! Comece novamente.", ephemeral=True)
            return
        
        CONTEXTO_USUARIO[user_id]['botao'] = botao
        opcao = CONTEXTO_USUARIO[user_id]['opcao']
        
        mensagens = {
            "link": f"🔗 Envie o link para o **Botão {botao}**:",
            "video": f"🎥 Envie o vídeo para o **Botão {botao}**:",
            "imagem": f"🖼️ Envie a imagem para o **Botão {botao}**:",
            "conteudo": f"📁 Envie os dados para o **Botão {botao}**:"
        }
        
        embed = discord.Embed(
            title=mensagens.get(opcao, "Pronto!"),
            description="Aguardando seu envio...",
            color=discord.Color.blue()
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    except Exception as e:
        log.error(f"Erro em processar_escolha_botao: {e}", exc_info=True)
        try:
            await interaction.followup.send(f"❌ Erro: {str(e)}", ephemeral=True)
        except:
            pass

async def processar_arquivo_usuario(message: discord.Message, user_id: int, opcao: str, botao: int):
    """Processa arquivo enviado pelo usuário (anexo ou URL)"""
    try:
        from arquivo_processor import processar_arquivo, eh_arquivo_compactado, extrair_arquivo_compactado
        from database import listar_chaves_ativas
        import tempfile
        
        # ============ ARQUIVO ANEXADO ============
        if message.attachments:
            attachment = message.attachments[0]
            tipos_permitidos = {
                'video': ['.mp4', '.mkv', '.avi', '.mov', '.webm', '.bin'],
                'imagem': ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.bin'],
                'zip': ['.zip', '.rar', '.7z']  # Arquivos compactados
            }
            
            ext = os.path.splitext(attachment.filename.lower())[1]
            
            # Verificar se é arquivo compactado
            eh_compactado = eh_arquivo_compactado(attachment.filename)
            
            if eh_compactado:
                # Aceitar arquivo compactado para qualquer tipo
                pass
            elif opcao not in tipos_permitidos or ext not in tipos_permitidos.get(opcao, []):
                await message.reply(f"❌ Tipo inválido! Para {opcao}: {', '.join(tipos_permitidos[opcao])}", mention_author=False)
                return
            
            await message.reply("⏳ Processando arquivo...", mention_author=False)
            
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                temp_path = tmp.name
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as resp:
                        tmp.write(await resp.read())
            
            print(f"📥 Arquivo: {attachment.filename} ({attachment.size / (1024*1024):.1f}MB)")
            
            # Se é compactado, extrair e filtrar
            if eh_compactado:
                print(f"📦 Detectado arquivo compactado: {attachment.filename}")
                arquivo_processado = extrair_arquivo_compactado(temp_path, opcao)
                if not arquivo_processado:
                    await message.reply(f"❌ Erro ao extrair arquivo compactado ou nenhum arquivo do tipo '{opcao}' encontrado", mention_author=False)
                    try:
                        os.remove(temp_path)
                    except:
                        pass
                    return
                print(f"✅ Arquivo extraído e filtrado: {arquivo_processado}")
            else:
                arquivo_processado = processar_arquivo(temp_path, opcao, botao)
            
            try:
                os.remove(temp_path)
            except:
                pass
            
            if not arquivo_processado:
                await message.reply("❌ Erro ao processar arquivo", mention_author=False)
                return
            
            nome_arquivo = os.path.basename(arquivo_processado)
            chaves = listar_chaves_ativas()
            chave_usuario = None
            for c in chaves:
                if c['user_id'] == user_id:
                    chave_usuario = c['chave']
                    break
            
            if chave_usuario:
                # Registrar com indicação se foi extraído
                dados_atualizacao = {'conteudo': nome_arquivo}
                if eh_compactado:
                    dados_atualizacao['extraido_de'] = attachment.filename
                registrar_atualizacao(chave_usuario, opcao, botao, dados_atualizacao)
                print(f"✅ Arquivo registrado: {nome_arquivo}")
            
            tamanho = os.path.getsize(arquivo_processado) / (1024 * 1024)
            
            descricao = f"**Botão {botao + 1}**\n📁 {nome_arquivo}\n📊 {tamanho:.1f}MB\n✨ Sincronizado!\n\n💡 *Se você já tinha enviado outro arquivo para este botão, o anterior foi descartado automaticamente.*"
            if eh_compactado:
                descricao += f"\n\n📦 *Extraído de: {attachment.filename}*"
            
            embed = discord.Embed(
                title="✅ ATUALIZADO!",
                description=descricao,
                color=discord.Color.green()
            )
            await message.reply(embed=embed, mention_author=False)
            
            # LIMPEZA DO CANAL: Deletar mensagens antigas, manter apenas a última
            try:
                await limpar_canal_manter_ultima(message.channel)
            except Exception as e:
                print(f"⚠️ Erro ao limpar canal: {e}")
        
        # ============ URL ENVIADA ============
        elif re.search(r'https?://', message.content):
            urls = re.findall(r'https?://[^\s]+', message.content)
            if urls:
                await processar_url_usuario(message, user_id, opcao, botao, urls[0])
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        log.error(f"❌ Erro ao processar arquivo: {e}", exc_info=True)
        await message.reply(f"❌ Erro: {str(e)}", mention_author=False)


async def processar_url_usuario(message: discord.Message, user_id: int, opcao: str, botao: int, url: str):
    """Processa download de arquivo a partir de URL"""
    try:
        from arquivo_processor import processar_arquivo
        from database import listar_chaves_ativas
        import tempfile
        
        tipos_permitidos = {
            'video': ['.mp4', '.mkv', '.avi', '.mov', '.webm', '.bin'],
            'imagem': ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.bin']
        }
        
        embed_status = discord.Embed(
            title="📥 INICIANDO DOWNLOAD",
            description=f"🔗 URL: {url[:60]}...\n⏳ Fazendo download...",
            color=discord.Color.blue()
        )
        msg = await message.reply(embed=embed_status, mention_author=False)
        
        # Fazer download
        print(f"📥 Iniciando download de: {url}")
        log.info(f"📥 URL detectada para botão {botao}: {url}")
        
        # Extrair nome original da URL
        from urllib.parse import urlparse
        import unicodedata
        
        parsed_url = urlparse(url)
        nome_url = os.path.basename(parsed_url.path)
        
        # Se não tiver nome, usar genérico
        if not nome_url or '=' in url:
            nome_url = f"arquivo_botao_{botao + 1}"
        
        # Limpar nome
        nome_url = unicodedata.normalize('NFKD', nome_url)
        nome_url = nome_url.encode('ascii', 'ignore').decode('ascii')
        nome_url = re.sub(r'[<>:"/\\|?*]', '_', nome_url)
        nome_url = os.path.splitext(nome_url)[0]  # Remove extensão (será adicionada depois)
        
        # Fazer download com nome genérico
        arquivo_path = await download_arquivo(url, f"temp_{botao}.bin", botao)
        
        if not arquivo_path:
            await msg.edit(embed=discord.Embed(
                title="❌ ERRO NO DOWNLOAD",
                description="Não foi possível fazer download",
                color=discord.Color.red()
            ))
            return
        
        # Validar extensão
        ext = os.path.splitext(arquivo_path)[1].lower()
        if opcao not in tipos_permitidos or ext not in tipos_permitidos.get(opcao, []):
            os.remove(arquivo_path)
            await msg.edit(embed=discord.Embed(
                title="❌ TIPO NÃO PERMITIDO",
                description=f"Para {opcao}: {', '.join(tipos_permitidos[opcao])}",
                color=discord.Color.red()
            ))
            return
        
        # ❓ PERGUNTAR AO USUÁRIO O NOME QUE ELE QUER DAR AO BOTÃO
        embed_pergunta = discord.Embed(
            title="📝 QUAL NOME VOCÊ QUER PARA ESTE BOTÃO?",
            description=f"Envie o nome que deseja exibir no botão.\n\n"
                        f"**Sugestão:** {nome_url}\n\n"
                        f"*(Deixe em branco para usar a sugestão automaticamente)*",
            color=discord.Color.blue()
        )
        await msg.edit(embed=embed_pergunta)
        
        # Aguardar resposta do usuário
        try:
            resposta = await bot.wait_for(
                'message',
                check=lambda m: m.author.id == user_id and m.guild.id == message.guild.id,
                timeout=60.0
            )
            
            # Obter nome fornecido ou usar sugestão
            nome_fornecido = resposta.content.strip()
            if nome_fornecido:
                nome_final = nome_fornecido
                print(f"✅ Usuário digitou nome: {nome_final}")
                log.info(f"✅ Usuário digitou nome: {nome_final}")
            else:
                nome_final = nome_url
                print(f"✅ Usando nome sugerido: {nome_final}")
                log.info(f"✅ Usando nome sugerido: {nome_final}")
            
            # Deletar mensagem do usuário
            try:
                await resposta.delete()
            except:
                pass
                
        except asyncio.TimeoutError:
            # Se timeout, usar sugestão automaticamente
            nome_final = nome_url
            print(f"⏱️ Timeout! Usando nome sugerido: {nome_final}")
            log.info(f"⏱️ Timeout! Usando nome sugerido: {nome_final}")
            await msg.edit(embed=discord.Embed(
                title="⏱️ TIMEOUT",
                description=f"Você não respondeu a tempo. Usando: **{nome_final}**",
                color=discord.Color.orange()
            ))
            await asyncio.sleep(2)
        
        print(f"✅ Arquivo será salvo com nome: {nome_final}")
        log.info(f"✅ Arquivo será salvo com nome: {nome_final}")
        
        await continuar_processamento_url(
            arquivo_path, opcao, botao, user_id, 
            nome_final, tipos_permitidos, msg
        )
        
    except Exception as e:
        print(f"❌ Erro ao processar URL: {e}")
        log.error(f"❌ Erro ao processar URL: {e}", exc_info=True)
        await message.reply(f"❌ Erro: {str(e)}", mention_author=False)

# ============================================================
# EVENTOS
# ============================================================

@bot.event
async def on_guild_join(guild):
    try:
        for canal in guild.text_channels:
            if canal.name == "smindeck":
                embed = discord.Embed(
                    title="🎉 BEM-VINDO AO SMINDECK! 🎉",
                    description="Sou seu assistente virtual! 🤖",
                    color=discord.Color.gold()
                )
                await canal.send(embed=embed)
                return
        
        channel = await guild.create_text_channel(name="smindeck", topic="🤖 Assistente Virtual SminDeck")
        embed = discord.Embed(
            title="🎉 BEM-VINDO AO SMINDECK! 🎉",
            description="Sou seu assistente virtual! 🤖",
            color=discord.Color.gold()
        )
        await channel.send(embed=embed)
    except:
        pass

@bot.event
async def on_message(message):
    # Ignorar mensagens do próprio bot/outros bots e DMs (mantém o fluxo só em servidor)
    if getattr(message.author, 'bot', False) or message.guild is None:
        log.info(f"🚫 Mensagem ignorada (bot ou DM): {message.author}")
        await bot.process_commands(message)
        return

    log.info(f"✅ NOVA MENSAGEM RECEBIDA: {message.author} → {message.content}")
    print(f"\n📩 MESSAGE: {message.author} → {message.content}")
    log.info(f"📩 MESSAGE: {message.author} → {message.content}")
    
    user_id = message.author.id
    guild_id = message.guild.id
    content = message.content.strip()
    
    print(f"👤 User: {user_id} | Guild: {guild_id} | Channel: {message.channel.id}")
    print(f"🔐 Autenticado?: {usuario_autenticado(user_id)}")
    log.info(f"👤 User: {user_id} | Guild: {guild_id} | Autenticado?: {usuario_autenticado(user_id)}")
    
    # ============ NÃO AUTENTICADO ============
    if not usuario_autenticado(user_id):
        print(f"🔐 Usuário NÃO autenticado. Conteúdo: {content}")
        log.info(f"🔐 Usuário NÃO autenticado. Conteúdo: {content}")
        
        # Gerar chave (APENAS com "oi")
        if content.lower() == "oi":
            print(f"✅ Requisição de chave detectada! Gerando e autenticando...")
            log.info(f"✅ Requisição de chave detectada para user {user_id}")
            try:
                # Gera a chave E autentica automaticamente no banco
                chave = criar_chave(user_id, guild_id, message.channel.id)
                
                if chave:
                    embed = discord.Embed(
                        title="🔐 CHAVE DE AUTENTICAÇÃO",
                        description=f"Sua chave é:\n\n**{chave}**\n\n✅ Já foi autenticada!\n\nCopie esta chave e coloque no APP para sincronizar.",
                        color=discord.Color.green()
                    )
                    embed.set_footer(text="⏰ Válida por 5 minutos")
                    
                    await message.reply(embed=embed, mention_author=False)
                    print(f"✅ Chave enviada para {user_id}")
                    log.info(f"✅ Chave enviada para {user_id}")
                    return  # 🛑 Sair - usuário digita "oi" de novo para menu
                else:
                    await message.reply("❌ Erro ao gerar chave. Tente novamente.", mention_author=False)
                    log.error(f"❌ criar_chave() retornou None para user {user_id}")
                    return  # 🛑 Sair se erro
            except Exception as e:
                print(f"❌ Erro ao gerar chave: {e}")
                log.error(f"❌ Erro ao gerar chave: {e}")
        else:
            # Se mandar qualquer coisa que não seja "oi", ignora
            print(f"⏭️ Mensagem ignorada (não é 'oi'): {content}")
            log.info(f"⏭️ Mensagem ignorada: {content}")
    
    # ============ AUTENTICADO - PROCESSAR DADOS ============
    else:
        # Se usuário autenticado mandar "oi", mostra o menu principal
        if content.lower() == "oi":
            print(f"✅ Usuário autenticado pediu menu (oi)")
            log.info(f"✅ Usuário autenticado {user_id} pediu menu")
            try:
                await mostrar_menu_principal(message.channel)
                print(f"✅ Menu enviado com sucesso!")
                log.info(f"✅ Menu enviado com sucesso!")
            except Exception as e:
                print(f"❌ Erro ao mostrar menu: {e}")
                log.error(f"❌ Erro ao mostrar menu: {e}")
            return
        
        if user_id in CONTEXTO_USUARIO:
            ctx = CONTEXTO_USUARIO[user_id]
            
            # ⏰ Verificar se o contexto expirou (mais de 5 minutos)
            if time.time() - ctx.get('timestamp', time.time()) > CONTEXT_TIMEOUT:
                print(f"⏱️ Contexto expirado para user {user_id} (mais de 5 minutos)")
                log.warning(f"⏱️ Contexto expirado para user {user_id}")
                await message.reply("❌ Sessão expirada! Envie 'oi' de novo para começar.", mention_author=False)
                del CONTEXTO_USUARIO[user_id]
                return
            
            # Se tem botão e opção, está recebendo dados
            if ctx['botao'] and ctx['opcao']:
                opcao = ctx['opcao']
                botao = ctx['botao']
                
                # 📎 VERIFICAR SE TEM ANEXO (ARQUIVO)
                if message.attachments:
                    print(f"📎 Anexo detectado! Processando arquivo...")
                    await processar_arquivo_usuario(message, user_id, opcao, int(botao))
                    del CONTEXTO_USUARIO[user_id]
                    return
                
                # 🔗 VERIFICAR SE TEM URL
                if re.search(r'https?://', content):
                    print(f"🔗 URL detectada! Processando download...")
                    urls = re.findall(r'https?://[^\s]+', content)
                    if urls:
                        await processar_url_usuario(message, user_id, opcao, int(botao), urls[0])
                        del CONTEXTO_USUARIO[user_id]
                        return
                
                # ✅ Registrar atualização de texto no banco de dados
                try:
                    # Obter a chave do usuário autenticado
                    from database import listar_chaves_ativas
                    chaves = listar_chaves_ativas()
                    chave_usuario = None
                    for c in chaves:
                        if c['user_id'] == user_id:
                            chave_usuario = c['chave']
                            break
                    
                    if chave_usuario:
                        registrar_atualizacao(chave_usuario, opcao, int(botao), {'conteudo': content})
                        print(f"✅ Atualização registrada: Botão {botao} | Tipo: {opcao}")
                        log.info(f"✅ Atualização registrada: Botão {botao} | Tipo: {opcao}")
                except Exception as e:
                    print(f"⚠️ Aviso ao registrar atualização: {e}")
                    log.warning(f"⚠️ Aviso ao registrar atualização: {e}")
                
                embed = discord.Embed(
                    title="✅ SUCESSO!",
                    description=f"Seus dados foram atualizados no **Botão {botao}**!\n\n**{content[:80]}...**\n\n✨ Tudo pronto!",
                    color=discord.Color.green()
                )
                await message.reply(embed=embed, mention_author=False)
                
                # Limpar contexto do usuário
                del CONTEXTO_USUARIO[user_id]
                
                # ❌ NÃO mostrar menu automaticamente
                # Esperar o cliente enviar "oi" de novo


@bot.tree.command(name="status", description="Status do bot")
async def status_cmd(interaction: discord.Interaction):
    embed = discord.Embed(title="🟢 BOT ONLINE", description="Tudo funcionando!", color=discord.Color.green())
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ✅ LIMPEZA PERIÓDICA DE CONTEXTOS EXPIRADOS
@tasks.loop(minutes=1)  # Verificar a cada minuto
async def limpar_contextos_expirados():
    """Remove contextos de usuário que expiraram"""
    agora = time.time()
    usuarios_expirados = []
    
    for user_id, ctx in CONTEXTO_USUARIO.items():
        if agora - ctx.get('timestamp', agora) > CONTEXT_TIMEOUT:
            usuarios_expirados.append(user_id)
            print(f"🧹 Limpando contexto expirado de user {user_id}")
    
    for user_id in usuarios_expirados:
        del CONTEXTO_USUARIO[user_id]
    
    if usuarios_expirados:
        log.info(f"🧹 {len(usuarios_expirados)} contexto(s) expirado(s) removido(s)")

@bot.event
async def on_ready():
    """Evento de inicialização - init DB + carrega autenticações + inicia limpeza periódica"""
    print(f"\n{'='*50}")
    print(f"✅ Bot Online: {bot.user}")
    print(f"{'='*50}\n")

    # Inicializar banco de dados
    init_database()
    print("✅ Banco de dados inicializado")

    # Carregar usuários autenticados do arquivo (compatibilidade)
    try:
        if os.path.exists(AUTHENTICATED_FILE):
            with open(AUTHENTICATED_FILE, 'r') as f:
                data = json.load(f)
                for user_id_str, info in data.items():
                    user_id = int(user_id_str)
                    USUARIOS_AUTENTICADOS[user_id] = info
                    USER_CHANNELS[user_id] = info.get('channel_id')
            print(f"✅ {len(USUARIOS_AUTENTICADOS)} usuários autenticados carregados")
    except Exception as e:
        print(f"⚠️ Erro ao carregar autenticações: {e}")

    # Iniciar tarefa de limpeza se ainda não estiver rodando
    if not limpar_contextos_expirados.is_running():
        limpar_contextos_expirados.start()

def main():
    print("\n" + "="*50)
    print("🤖 SminDeck Assistente Virtual")
    print("="*50 + "\n")
    
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
