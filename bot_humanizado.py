# Bot Discord Humanizado - Mensagens Amigáveis e Intuitivas

import discord
from discord.ext import commands
from discord import app_commands
import random

class BotHumanizado(commands.Cog):
    """Cog com personalidade humanizada do bot"""
    
    def __init__(self, bot):
        self.bot = bot
        self.greetings = [
            "Oi! 👋",
            "Olá! 😊",
            "E aí! 🙌",
            "Tudo bem? 👍",
            "Opa! 🎉",
            "Salve! 🚀"
        ]
    
    # =============================================
    # 🎮 COMANDO PRINCIPAL - MENU INTUITIVO
    # =============================================
    
    @app_commands.command(name="help", description="Em que posso te ajudar?")
    async def help_humanized(self, interaction: discord.Interaction):
        """Menu principal com opções"""
        
        greeting = random.choice(self.greetings)
        
        embed = discord.Embed(
            title=f"{greeting} Bem-vindo ao SminBot!",
            description="Que tal eu te ajudar agora? Escolha uma opção abaixo! 😊",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="📽️ Atualizações Disponíveis",
            value=(
                "• **🔗 Atualizar Link** - Adicione novo URL de vídeo\n"
                "• **🎥 Atualizar Vídeo** - Troque o vídeo de um botão\n"
                "• **🖼️ Atualizar Imagem** - Atualize uma imagem\n"
                "• **� Enviar Arquivo** - Compartilhe arquivo (vai para pasta geral do app)"
            ),
            inline=False
        )
        
        embed.add_field(
            name="💡 Dica",
            value="Use os botões abaixo para escolher o que quer fazer!",
            inline=False
        )
        
        embed.set_footer(text="SminBot | Sempre aqui para ajudar! 🤖")
        
        view = MenuPrincipal()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=False)
    
    # =============================================
    # 👋 BOAS-VINDAS NA SALA
    # =============================================
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Responde quando alguém manda 'ola' ou similar"""
        
        if message.author == self.bot.user:
            return
        
        msg_lower = message.content.lower().strip()
        
        # Responder a cumprimentos
        if msg_lower in ["ola", "olá", "oi", "e aí", "salve", "tudo bem"]:
            greeting = random.choice(self.greetings)
            responses = [
                f"{greeting} Bem-vindo à sala! 😊 Como posso ajudar?",
                f"{greeting} Fico feliz em te ver! 🎉 O que precisa?",
                f"{greeting} Sempre pronto para ajudar! 💪 Em que posso ser útil?",
                f"{greeting} Que bom te ver! 👋 O que deseja fazer hoje?"
            ]
            response = random.choice(responses)
            await message.reply(response)
        
        # Se for comando, processar normalmente
        await self.bot.process_commands(message)


# =============================================
# 🎛️ MENU COM BOTÕES (BUTTONS)
# =============================================

class MenuPrincipal(discord.ui.View):
    """View com botões do menu principal"""
    
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="🔗 Atualizar Link", style=discord.ButtonStyle.blurple)
    async def atualizar_link(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para atualizar link"""
        embed = discord.Embed(
            title="🔗 Atualizar Link",
            description="Qual botão você quer atualizar?\n\nUse: `/atualizar_link [numero] [novo_url]`",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Exemplo",
            value="`/atualizar_link 1 https://youtu.be/novo_video`",
            inline=False
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="🎥 Atualizar Vídeo", style=discord.ButtonStyle.blurple)
    async def atualizar_video(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para atualizar vídeo"""
        embed = discord.Embed(
            title="🎥 Atualizar Vídeo",
            description="Qual é o novo vídeo?\n\nUse: `/atualizar_video [numero] [arquivo]`",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Formato Aceito",
            value="MP4, WebM, ou link de streaming",
            inline=False
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="🖼️ Atualizar Imagem", style=discord.ButtonStyle.blurple)
    async def atualizar_imagem(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para atualizar imagem"""
        embed = discord.Embed(
            title="🖼️ Atualizar Imagem",
            description="Qual imagem você quer atualizar?\n\nUse: `/atualizar_imagem [numero] [arquivo]`",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Formato Aceito",
            value="PNG, JPG, GIF, WebP",
            inline=False
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label=" Enviar Arquivo", style=discord.ButtonStyle.danger)
    async def enviar_arquivo(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para enviar arquivo"""
        embed = discord.Embed(
            title="💾 Enviar Arquivo para Content Menu",
            description="Quer compartilhar um arquivo com a galera? 📤",
            color=discord.Color.purple()
        )
        embed.add_field(
            name="Como enviar?",
            value="1. Clique em **[+]** ao lado do campo de mensagem\n"
                  "2. Escolha **Enviar arquivo** ou **Fazer upload de arquivo**\n"
                  "3. Selecione o arquivo\n"
                  "4. Envie aqui no Discord\n\n"
                  "✨ Será salvo automaticamente na pasta **Arquivos Gerais** do app!\n"
                  "📂 Você poderá acessar via drag-drop ou adicionar como mídia!",
            inline=False
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


# =============================================
# 🔄 COMANDOS DE ATUALIZAÇÃO
# =============================================

async def setup(bot):
    """Setup do cog"""
    await bot.add_cog(BotHumanizado(bot))


# Exemplo de como integrar no bot principal:
"""
# No discord_bot.py principal:

from bot_humanizado import BotHumanizado

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    await bot.load_extension('bot_humanizado')

"""

if __name__ == "__main__":
    print("Este módulo é para usar como Cog no bot principal")
