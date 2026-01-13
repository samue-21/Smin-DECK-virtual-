# Bot Discord Humanizado - Fluxo Interativo com Perguntas

import discord
from discord.ext import commands
from discord import app_commands
import random

class BotHumanizadoInterativo(commands.Cog):
    """Cog com personalidade humanizada e fluxo interativo"""
    
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
                "• **💾 Enviar Arquivo** - Compartilhe arquivo (vai para pasta geral do app)"
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
        """Responde quando alguém manda 'ola' ou similar e mostra o menu"""
        
        if message.author == self.bot.user:
            return
        
        msg_lower = message.content.lower().strip()
        
        # Responder a cumprimentos COM MENU
        if msg_lower in ["ola", "olá", "oi", "e aí", "salve", "tudo bem", "oi tudo bem", "como vai", "oie"]:
            greeting = random.choice(self.greetings)
            
            # Criar embed com menu
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
                    "• **💾 Enviar Arquivo** - Compartilhe arquivo (vai para pasta geral do app)"
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
            await message.reply(embed=embed, view=view, mention_author=True)
        
        # Se for comando, processar normalmente
        await self.bot.process_commands(message)


# =============================================
# 📝 MODAIS INTERATIVOS - PERGUNTAS
# =============================================

class ModalEscolherBotao(discord.ui.Modal):
    """Modal para escolher qual botão atualizar"""
    
    botao_numero = discord.ui.TextInput(
        label="📌 Qual botão você quer atualizar?",
        placeholder="Digite o número (1-12, ex: 5)",
        min_length=1,
        max_length=2,
        required=True
    )
    
    def __init__(self, tipo_atualizacao: str, parent_view):
        super().__init__(title=f"Atualizar {tipo_atualizacao}")
        self.tipo_atualizacao = tipo_atualizacao
        self.parent_view = parent_view
    
    async def on_submit(self, interaction: discord.Interaction):
        """Processa a resposta"""
        
        try:
            numero = int(self.botao_numero.value)
            
            # Validar se está entre 1-12
            if numero < 1 or numero > 12:
                embed = discord.Embed(
                    title="❌ Número Inválido",
                    description="Por favor, escolha um número entre **1 e 12**! 🎯",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            # Guardar número escolhido
            self.parent_view.botao_escolhido = numero
            
            # Próxima pergunta conforme o tipo
            if self.tipo_atualizacao == "Link":
                await self._pergunta_url(interaction, numero)
            elif self.tipo_atualizacao == "Vídeo":
                await self._pergunta_video(interaction, numero)
            elif self.tipo_atualizacao == "Imagem":
                await self._pergunta_imagem(interaction, numero)
        
        except ValueError:
            embed = discord.Embed(
                title="❌ Número Inválido",
                description="Por favor, digite um número! (exemplo: 5) 🔢",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def _pergunta_url(self, interaction: discord.Interaction, numero: int):
        """Pergunta qual URL novo"""
        
        embed = discord.Embed(
            title="🔗 Qual é a Nova URL?",
            description=f"Você escolheu o **Botão {numero}**\n\n"
                        "Qual é a nova URL/link que você quer adicionar?\n"
                        "(exemplo: https://youtu.be/video123 ou https://seu-site.com)",
            color=discord.Color.green()
        )
        embed.add_field(
            name="💡 Dica",
            value="Pode ser YouTube, link do seu site, ou qualquer outro URL!",
            inline=False
        )
        
        # Criar modal para a URL
        modal = ModalPerguntaURL(numero, self.parent_view)
        await interaction.response.send_modal(modal)
    
    async def _pergunta_video(self, interaction: discord.Interaction, numero: int):
        """Pergunta qual vídeo novo"""
        
        embed = discord.Embed(
            title="🎥 Qual é o Novo Vídeo?",
            description=f"Você escolheu o **Botão {numero}**\n\n"
                        "Qual é o novo vídeo que você quer adicionar?\n"
                        "(arquivo MP4, WebM ou link de streaming)",
            color=discord.Color.green()
        )
        embed.add_field(
            name="📁 Formatos Aceitos",
            value="MP4, WebM, ou link de video (YouTube, Vimeo, etc)",
            inline=False
        )
        
        modal = ModalPerguntaVideo(numero, self.parent_view)
        await interaction.response.send_modal(modal)
    
    async def _pergunta_imagem(self, interaction: discord.Interaction, numero: int):
        """Pergunta qual imagem nova"""
        
        embed = discord.Embed(
            title="🖼️ Qual é a Nova Imagem?",
            description=f"Você escolheu o **Botão {numero}**\n\n"
                        "Qual é a nova imagem que você quer adicionar?\n"
                        "(arquivo PNG, JPG, GIF ou WebP)",
            color=discord.Color.green()
        )
        embed.add_field(
            name="🎨 Formatos Aceitos",
            value="PNG, JPG, JPEG, GIF, WebP",
            inline=False
        )
        
        modal = ModalPerguntaImagem(numero, self.parent_view)
        await interaction.response.send_modal(modal)


class ModalPerguntaURL(discord.ui.Modal):
    """Modal para digitar a URL"""
    
    url_input = discord.ui.TextInput(
        label="Cole a URL aqui",
        placeholder="https://youtu.be/...",
        min_length=10,
        max_length=500,
        required=True
    )
    
    def __init__(self, numero_botao: int, parent_view):
        super().__init__(title="Nova URL")
        self.numero_botao = numero_botao
        self.parent_view = parent_view
    
    async def on_submit(self, interaction: discord.Interaction):
        """Processa a URL"""
        
        url = self.url_input.value.strip()
        
        # Validar URL básica
        if not url.startswith(('http://', 'https://')):
            embed = discord.Embed(
                title="❌ URL Inválida",
                description="A URL deve começar com `http://` ou `https://`! 🔗",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Confirmação
        await self._confirmar(interaction, url)
    
    async def _confirmar(self, interaction: discord.Interaction, url: str):
        """Mostra confirmação final"""
        
        embed = discord.Embed(
            title="✅ Tudo Prontinho!",
            description=f"Em alguns minutos o **Link** do **Botão {self.numero_botao}** estará atualizado!\n\n"
                        f"🔗 Nova URL:\n`{url}`",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="🎯 O que foi feito?",
            value=f"• Botão escolhido: **{self.numero_botao}** ✅\n"
              f"• Tipo: **Link** ✅\n"
                  f"• Status: **Em processamento...** ⏳",
            inline=False
        )
        
        # Mensagem de agradecimento
        embed.add_field(
            name="🙏 Obrigado!",
            value="Muito obrigado por usar o SminBot! 🤖\n"
                  "Seu link será atualizado em breve! ⚡",
            inline=False
        )
        
        embed.set_footer(text="SminBot | Sempre aqui para ajudar!")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


class ModalPerguntaVideo(discord.ui.Modal):
    """Modal para digitar o vídeo"""
    
    video_input = discord.ui.TextInput(
        label="Cole o link ou nome do arquivo",
        placeholder="arquivo.mp4 ou https://...",
        min_length=5,
        max_length=500,
        required=True
    )
    
    def __init__(self, numero_botao: int, parent_view):
        super().__init__(title="Novo Vídeo")
        self.numero_botao = numero_botao
        self.parent_view = parent_view
    
    async def on_submit(self, interaction: discord.Interaction):
        """Processa o vídeo"""
        
        video = self.video_input.value.strip()
        
        # Validar extensão
        extensoes_validas = ['.mp4', '.webm', '.avi', '.mov']
        links_validos = ['youtube', 'youtu.be', 'vimeo', 'twitch']
        
        valido = any(ext in video.lower() for ext in extensoes_validas) or \
                 any(link in video.lower() for link in links_validos) or \
                 video.startswith(('http://', 'https://'))
        
        if not valido:
            embed = discord.Embed(
                title="❌ Vídeo Inválido",
                description="O vídeo deve ser um arquivo (MP4, WebM, etc) ou um link válido! 🎥",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await self._confirmar(interaction, video)
    
    async def _confirmar(self, interaction: discord.Interaction, video: str):
        """Mostra confirmação final"""
        
        embed = discord.Embed(
            title="✅ Tudo Prontinho!",
            description=f"Em alguns minutos o **Vídeo** do **Botão {self.numero_botao}** estará atualizado! 🎬\n\n"
                        f"🎥 Novo vídeo:\n`{video}`",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="🎯 O que foi feito?",
            value=f"• Botão escolhido: **{self.numero_botao}** ✅\n"
                  f"• Tipo: **Vídeo** ✅\n"
                  f"• Status: **Em processamento...** ⏳",
            inline=False
        )
        
        embed.add_field(
            name="🙏 Obrigado!",
            value="Muito obrigado por usar o SminBot! 🤖\n"
                  "Seu vídeo será atualizado em breve! ⚡",
            inline=False
        )
        
        embed.set_footer(text="SminBot | Sempre aqui para ajudar!")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


class ModalPerguntaImagem(discord.ui.Modal):
    """Modal para digitar a imagem"""
    
    imagem_input = discord.ui.TextInput(
        label="Cole o link ou nome do arquivo",
        placeholder="imagem.png ou https://...",
        min_length=5,
        max_length=500,
        required=True
    )
    
    def __init__(self, numero_botao: int, parent_view):
        super().__init__(title="Nova Imagem")
        self.numero_botao = numero_botao
        self.parent_view = parent_view
    
    async def on_submit(self, interaction: discord.Interaction):
        """Processa a imagem"""
        
        imagem = self.imagem_input.value.strip()
        
        # Validar extensão
        extensoes_validas = ['.png', '.jpg', '.jpeg', '.gif', '.webp']
        
        valido = any(ext in imagem.lower() for ext in extensoes_validas) or \
                 imagem.startswith(('http://', 'https://'))
        
        if not valido:
            embed = discord.Embed(
                title="❌ Imagem Inválida",
                description="A imagem deve ser PNG, JPG, GIF, WebP ou um link válido! 🖼️",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await self._confirmar(interaction, imagem)
    
    async def _confirmar(self, interaction: discord.Interaction, imagem: str):
        """Mostra confirmação final"""
        
        embed = discord.Embed(
            title="✅ Tudo Prontinho!",
            description=f"Em alguns minutos a **Imagem** do **Botão {self.numero_botao}** estará atualizada! 🎨\n\n"
                        f"🖼️ Nova imagem:\n`{imagem}`",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="🎯 O que foi feito?",
            value=f"• Botão escolhido: **{self.numero_botao}** ✅\n"
                  f"• Tipo: **Imagem** ✅\n"
                  f"• Status: **Em processamento...** ⏳",
            inline=False
        )
        
        embed.add_field(
            name="🙏 Obrigado!",
            value="Muito obrigado por usar o SminBot! 🤖\n"
                  "Sua imagem será atualizada em breve! ⚡",
            inline=False
        )
        
        embed.set_footer(text="SminBot | Sempre aqui para ajudar!")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


# =============================================
# 🎛️ MENU COM BOTÕES (BUTTONS)
# =============================================

class MenuPrincipal(discord.ui.View):
    """View com botões do menu principal"""
    
    def __init__(self):
        super().__init__(timeout=None)
        self.botao_escolhido = None
    
    @discord.ui.button(label="🔗 Atualizar Link", style=discord.ButtonStyle.blurple)
    async def atualizar_link(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para atualizar link - Abre modal"""
        
        modal = ModalEscolherBotao("Link", self)
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="🎥 Atualizar Vídeo", style=discord.ButtonStyle.blurple)
    async def atualizar_video(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para atualizar vídeo - Abre modal"""
        
        modal = ModalEscolherBotao("Vídeo", self)
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="🖼️ Atualizar Imagem", style=discord.ButtonStyle.blurple)
    async def atualizar_imagem(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para atualizar imagem - Abre modal"""
        
        modal = ModalEscolherBotao("Imagem", self)
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="💾 Enviar Arquivo", style=discord.ButtonStyle.danger)
    async def enviar_arquivo(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Botão para enviar arquivo"""
        embed = discord.Embed(
            title="💾 Enviar Arquivo para Pasta Geral",
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
# 🔄 SETUP
# =============================================

async def setup(bot):
    """Setup do cog"""
    await bot.add_cog(BotHumanizadoInterativo(bot))
