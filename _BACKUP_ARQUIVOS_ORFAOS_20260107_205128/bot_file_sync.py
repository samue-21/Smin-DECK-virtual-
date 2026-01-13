# Bot Discord - Sincronização de Arquivos com Pasta Local

import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class BotFileSync(commands.Cog):
    """Cog para sincronizar arquivos enviados no Discord com pasta local do app"""
    
    def __init__(self, bot, arquivos_gerais_path=None):
        self.bot = bot
        
        # Caminho da pasta "Arquivos Gerais"
        if arquivos_gerais_path is None:
            # Se não informado, tenta localizar automaticamente
            home = str(Path.home())
            self.arquivos_gerais_path = os.path.join(
                home, '.smindeckbot', 'arquivos_gerais'
            )
        else:
            self.arquivos_gerais_path = arquivos_gerais_path
        
        # Criar pasta se não existir
        os.makedirs(self.arquivos_gerais_path, exist_ok=True)
        logger.info(f"Pasta Arquivos Gerais: {self.arquivos_gerais_path}")
    
    # =============================================
    # 📥 LISTENER - DETECTA ARQUIVOS ENVIADOS
    # =============================================
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Detecta quando alguém envia um arquivo e sincroniza com pasta local"""
        
        # Ignorar mensagens do próprio bot
        if message.author == self.bot.user:
            return
        
        # Verificar se tem attachment (arquivo)
        if message.attachments:
            try:
                for attachment in message.attachments:
                    await self._baixar_arquivo(attachment, message.author.name)
                    
                # Confirmar recebimento
                await message.reply(
                    f"✅ {len(message.attachments)} arquivo(s) recebido(s)!\n"
                    f"📂 Foram salvos na pasta **Arquivos Gerais** do app!\n\n"
                    f"Você pode acessar:\n"
                    f"• Abrindo a pasta no app\n"
                    f"• Arrastar para editar botões (drag-drop)\n"
                    f"• Menu de adicionar mídia",
                    delete_after=10
                )
            except Exception as e:
                logger.error(f"Erro ao baixar arquivo: {e}")
                await message.reply(
                    "❌ Houve um erro ao processar o arquivo. Tente novamente!",
                    delete_after=5
                )
        
        # Processar comandos normalmente
        await self.bot.process_commands(message)
    
    # =============================================
    # 🔧 COMANDO - LISTAR ARQUIVOS LOCAIS
    # =============================================
    
    @app_commands.command(
        name="listar_arquivos",
        description="Veja todos os arquivos na pasta Arquivos Gerais"
    )
    async def listar_arquivos(self, interaction: discord.Interaction):
        """Lista todos os arquivos na pasta local"""
        
        try:
            files = []
            total_size = 0
            
            # Listar todos os arquivos
            for file in os.listdir(self.arquivos_gerais_path):
                file_path = os.path.join(self.arquivos_gerais_path, file)
                
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path)
                    size_mb = size / (1024 * 1024)
                    files.append({
                        'name': file,
                        'size': size_mb,
                        'size_str': f"{size_mb:.2f} MB"
                    })
                    total_size += size
            
            # Criar embed com lista
            embed = discord.Embed(
                title="📂 Arquivos Gerais",
                description=f"Total: {len(files)} arquivo(s)",
                color=discord.Color.blue()
            )
            
            if files:
                # Mostrar até 20 arquivos no embed
                file_list = ""
                for i, f in enumerate(files[:20], 1):
                    file_list += f"{i}. **{f['name']}** ({f['size_str']})\n"
                
                embed.add_field(
                    name="📋 Lista",
                    value=file_list if file_list else "Nenhum arquivo",
                    inline=False
                )
                
                embed.add_field(
                    name="📊 Total",
                    value=f"{len(files)} arquivo(s) | {total_size / (1024**2):.2f} MB",
                    inline=False
                )
                
                if len(files) > 20:
                    embed.add_field(
                        name="⚠️ Aviso",
                        value=f"Mostrando 20 de {len(files)} arquivos",
                        inline=False
                    )
            else:
                embed.add_field(
                    name="📭 Vazio",
                    value="Nenhum arquivo ainda. Envie um arquivo para começar! 📤",
                    inline=False
                )
            
            embed.set_footer(text="Abra a pasta no app para acessar todos os arquivos")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        except Exception as e:
            logger.error(f"Erro ao listar arquivos: {e}")
            await interaction.response.send_message(
                f"❌ Erro ao listar arquivos: {str(e)}",
                ephemeral=True
            )
    
    # =============================================
    # ⚙️ MÉTODO AUXILIAR - BAIXAR ARQUIVO
    # =============================================
    
    async def _baixar_arquivo(self, attachment, username):
        """
        Baixa arquivo do Discord e salva na pasta local
        
        Args:
            attachment: Discord attachment object
            username: Nome do usuário que enviou
        """
        
        # Criar nome único com timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Preservar extensão original
        nome_arquivo = f"{timestamp}_{attachment.filename}"
        arquivo_path = os.path.join(self.arquivos_gerais_path, nome_arquivo)
        
        # Baixar arquivo
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(attachment.url) as resp:
                    if resp.status == 200:
                        with open(arquivo_path, 'wb') as f:
                            f.write(await resp.read())
                        
                        logger.info(
                            f"✅ Arquivo baixado: {nome_arquivo} "
                            f"({attachment.size} bytes) "
                            f"por @{username}"
                        )
                    else:
                        logger.error(
                            f"Erro ao baixar: Status {resp.status} para {attachment.filename}"
                        )
        except Exception as e:
            logger.error(f"Erro ao baixar arquivo: {e}")
            raise
    
    # =============================================
    # 🗑️ COMANDO - LIMPAR ARQUIVOS ANTIGOS
    # =============================================
    
    @app_commands.command(
        name="limpar_arquivos",
        description="Remover todos os arquivos (⚠️ Cuidado!)"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def limpar_arquivos(self, interaction: discord.Interaction):
        """Remove todos os arquivos (apenas admin)"""
        
        try:
            count = 0
            for file in os.listdir(self.arquivos_gerais_path):
                file_path = os.path.join(self.arquivos_gerais_path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    count += 1
            
            await interaction.response.send_message(
                f"🗑️ {count} arquivo(s) removido(s)!",
                ephemeral=True
            )
        except Exception as e:
            logger.error(f"Erro ao limpar arquivos: {e}")
            await interaction.response.send_message(
                f"❌ Erro: {str(e)}",
                ephemeral=True
            )


# =============================================
# 📌 SETUP E INTEGRAÇÃO
# =============================================

async def setup(bot, arquivos_gerais_path=None):
    """Setup do cog"""
    await bot.add_cog(BotFileSync(bot, arquivos_gerais_path))


# Exemplo de como integrar no bot principal:
"""
# No discord_bot.py principal:

from bot_file_sync import BotFileSync

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    
    # Carregar cogs
    await bot.load_extension('bot_humanizado')
    
    # Carregar com caminho customizado (opcional)
    caminho_arquivos = os.path.expanduser('~/.smindeckbot/arquivos_gerais')
    await bot.load_extension('bot_file_sync')
    # ou: await BotFileSync.setup(bot, caminho_arquivos)

# Ou adicionar na inicialização do bot:
bot = commands.Bot(command_prefix='/', intents=intents)

# Antes de rodar:
# async def main():
#     async with bot:
#         await bot.load_extension('bot_humanizado')
#         await bot.load_extension('bot_file_sync')
#         await bot.start(TOKEN)

"""
