import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
from db import (
    DB_FILE,
    init_db,
    create_connection_key,
    get_connection_key,
    update_url,
    get_urls,
    set_default_button,
    get_default_button,
    get_default_button_optional,
    set_bot_channel,
    get_bot_channel,
)
import asyncio
import re
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Validar TOKEN
if not TOKEN:
    print("❌ ERRO: DISCORD_TOKEN não encontrado no arquivo .env")
    print("\n📝 Para configurar o bot:")
    print("1. Abra o arquivo .env na pasta de instalação do bot")
    print("2. Adicione a linha: DISCORD_TOKEN=seu_token_aqui")
    print("3. Salve o arquivo e reinicie o bot")
    print("\nPara obter um token:")
    print("- Acesse https://discord.com/developers/applications")
    print("- Clique em 'New Application'")
    print("- Vá para a aba 'Bot' e clique 'Add Bot'")
    print("- Copie o token (clique em 'Copy')")
    import time
    time.sleep(3)
    exit(1)

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Estado de conversa (por usuÃ¡rio/canal)
# key: (guild_id, channel_id, user_id) ->
#   - stage: "await_button" | "await_url"
#   - connection_key: str
#   - button: int
#   - expires: float
pending_url_requests = {}


async def ensure_dedicated_channel(guild: discord.Guild) -> discord.TextChannel | None:
    """Garante que existe um canal dedicado (ex: #smindeck) e salva no DB."""
    if not guild:
        return None

    server_id = str(guild.id)
    
    # Verificar se já temos um canal salvo
    stored_channel_id = get_bot_channel(server_id)
    if stored_channel_id:
        ch = guild.get_channel(int(stored_channel_id))
        if isinstance(ch, discord.TextChannel):
            print(f"✅ Canal já existe: {ch.name}")
            return ch

    # Procurar canal por nome
    for ch in guild.text_channels:
        if ch.name == "smindeck":
            print(f"✅ Canal encontrado por nome: {ch.name}")
            set_bot_channel(server_id, str(ch.id))
            return ch

    # Tentar criar novo canal
    try:
        print(f"🔨 Criando novo canal 'smindeck' no servidor {guild.name}...")
        
        # Verificar permissões
        me = guild.me
        if not me:
            print(f"❌ Bot sem acesso ao servidor")
            return None
        
        if not me.guild_permissions.manage_channels:
            print(f"❌ Bot sem permissão de 'manage_channels'")
            return None
        
        ch = await guild.create_text_channel(
            "smindeck",
            topic="Canal do SminDeck Bot - Configure seus comandos aqui",
            reason="Criado automaticamente pelo SminDeck Bot"
        )
        
        print(f"✅ Canal criado com sucesso: {ch.name}")
        set_bot_channel(server_id, str(ch.id))
        return ch
        
    except discord.Forbidden:
        print(f"❌ Sem permissão para criar canal (permissões insuficientes)")
        return None
    except discord.HTTPException as e:
        print(f"❌ Erro HTTP ao criar canal: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado ao criar canal: {e}")
        return None

# Inicializar banco de dados
init_db()

@bot.event
async def on_ready():
    print(f'âœ… Bot conectado como {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'âœ… Sincronizados {len(synced)} comandos slash')
    except Exception as e:
        print(f'âŒ Erro ao sincronizar: {e}')

    # Garantir canal dedicado em todos os servidores (best-effort)
    try:
        for g in bot.guilds:
            ch = await ensure_dedicated_channel(g)
            if ch:
                try:
                    await ch.send(
                        "âœ… SminDeck Bot ativo aqui. Diga **ola** para eu pedir a URL e atualizar o botÃ£o configurado."
                    )
                except Exception:
                    pass
    except Exception:
        pass


@bot.event
async def on_guild_join(guild: discord.Guild):
    # Quando o bot Ã© adicionado, cria/garante canal dedicado
    print(f"🤖 Bot adicionado ao servidor: {guild.name} (ID: {guild.id})")
    
    try:
        ch = await ensure_dedicated_channel(guild)
        if ch:
            print(f"✅ Canal criado/encontrado: {ch.name}")
            try:
                await ch.send(
                    "✅ Obrigado por me adicionar!\n\n"
                    "**Como usar:**\n"
                    "1. Digite aqui: `/setup`\n"
                    "2. Clique em 'New' para gerar uma chave de conexão\n"
                    "3. Use essa chave no SminDeck para conectar\n\n"
                    "Pronto! Agora você pode usar todos os comandos."
                )
            except Exception as e:
                print(f"❌ Erro ao enviar mensagem: {e}")
        else:
            print(f"❌ Não consegui criar o canal no servidor {guild.name}")
    except Exception as e:
        print(f"❌ Erro em on_guild_join: {e}")


def _normalize_text(text: str) -> str:
    text = (text or "").strip().lower()
    text = re.sub(r"\s+", " ", text)
    # remove pontuaÃ§Ã£o simples no fim
    text = re.sub(r"[!?.]+$", "", text)
    return text


def _looks_like_url(text: str) -> bool:
    t = (text or "").strip()
    return t.startswith("http://") or t.startswith("https://")


@bot.event
async def on_message(message: discord.Message):
    # Ignorar bots
    if message.author.bot:
        return

    # Apenas em servidor
    if not message.guild or not message.channel:
        return

    guild_id = str(message.guild.id)
    channel_id = str(message.channel.id)
    user_id = str(message.author.id)
    key_tuple = (guild_id, channel_id, user_id)

    # Restringir modo chat ao canal dedicado
    dedicated_channel_id = get_bot_channel(guild_id)
    if dedicated_channel_id and str(message.channel.id) != str(dedicated_channel_id):
        # Ignora totalmente fora do canal dedicado
        await bot.process_commands(message)
        return

    # Se usuÃ¡rio estÃ¡ em fluxo de "enviar URL"
    pending = pending_url_requests.get(key_tuple)
    if pending:
        # ExpiraÃ§Ã£o
        if pending.get("expires", 0) < time.time():
            pending_url_requests.pop(key_tuple, None)
        else:
            content = (message.content or "").strip()
            norm = _normalize_text(content)
            if norm in {"cancelar", "cancela", "sair"}:
                pending_url_requests.pop(key_tuple, None)
                await message.channel.send("âœ… Ok, cancelado. Quando quiser, diga **ola** de novo.")
                return

            stage = pending.get("stage")
            if stage == "await_button":
                # Espera um nÃºmero 1-12
                try:
                    btn = int(re.sub(r"[^0-9]", "", content))
                except Exception:
                    btn = None

                if not btn or not (1 <= btn <= 12):
                    await message.channel.send("âŒ Me diga o nÃºmero do botÃ£o (1 a 12), ou **cancelar**.")
                    return

                ok, err = set_default_button(guild_id, btn)
                if not ok:
                    pending_url_requests.pop(key_tuple, None)
                    await message.channel.send(f"âŒ NÃ£o consegui configurar o botÃ£o: {err}")
                    return

                pending["button"] = btn
                pending["stage"] = "await_url"
                pending["expires"] = time.time() + 180  # mais 3 minutos
                pending_url_requests[key_tuple] = pending

                await message.channel.send(
                    f"âœ… Perfeito. Agora me envie a URL do vÃ­deo para atualizar o **BotÃ£o {btn}** (ou **cancelar**)."
                )
                return

            if stage == "await_url" and (not _looks_like_url(content)):
                await message.channel.send("âŒ Me envie uma URL vÃ¡lida comeÃ§ando com `http://` ou `https://` (ou diga **cancelar**).")
                return

            if stage != "await_url":
                await message.channel.send("âŒ NÃ£o entendi. Diga **ola** para comeÃ§ar de novo.")
                return

            connection_key = pending["connection_key"]
            button_number = pending["button"]
            success, msg = update_url(connection_key.strip().upper(), button_number, content)

            pending_url_requests.pop(key_tuple, None)
            if success:
                await message.channel.send(
                    f"âœ… Atualizado! BotÃ£o **{button_number}** recebeu a nova URL. O SminDeck sincroniza em instantes."
                )
            else:
                await message.channel.send(f"âŒ NÃ£o consegui atualizar: {msg}")
            return

    # InÃ­cio do fluxo pelo chat
    norm = _normalize_text(message.content)
    greetings = {"ola", "olÃ¡", "oi", "eai", "e aÃ­", "bom dia", "boa tarde", "boa noite"}
    if norm in greetings:
        # 1) Garantir chave do servidor
        existing_key = get_connection_key(guild_id)
        created_now = False
        if existing_key:
            connection_key = existing_key
        else:
            connection_key = create_connection_key(guild_id)
            created_now = True

        # 2) Se criou agora, tenta mandar a chave por DM (pra nÃ£o vazar em canal)
        if created_now:
            try:
                await message.author.send(
                    f"ðŸ”‘ Sua chave do SminDeck (guarde com seguranÃ§a): `{connection_key}`\n"
                    "Cole essa chave no SminDeck para ele sincronizar as URLs."
                )
                await message.channel.send("ðŸ“© Te enviei a chave no privado. Agora vamos configurar o vÃ­deo aqui.")
            except Exception:
                await message.channel.send(
                    "âš ï¸ NÃ£o consegui te enviar DM com a chave. Ative DMs do servidor ou peÃ§a para um admin usar `/setup`."
                )

        # 3) Verificar se jÃ¡ existe botÃ£o padrÃ£o configurado
        button_number = get_default_button_optional(guild_id)
        if button_number is None:
            pending_url_requests[key_tuple] = {
                "stage": "await_button",
                "connection_key": connection_key,
                "button": 1,
                "expires": time.time() + 180,
            }
            await message.channel.send(
                "OlÃ¡! Antes de tudo: qual **nÃºmero do botÃ£o** vocÃª quer atualizar? (1 a 12)"
            )
            return

        pending_url_requests[key_tuple] = {
            "stage": "await_url",
            "connection_key": connection_key,
            "button": button_number,
            "expires": time.time() + 180,
        }

        await message.channel.send(
            f"OlÃ¡! Me envie agora a URL do vÃ­deo para atualizar o **BotÃ£o {button_number}** (ou diga **cancelar**)."
        )
        return

    # MantÃ©m comandos de prefixo funcionando (se houver)
    await bot.process_commands(message)


@bot.tree.command(name="canal", description="Define ESTE canal como o canal dedicado do SminDeck Bot")
async def set_channel(interaction: discord.Interaction):
    server_id = str(interaction.guild.id)
    ok, err = set_bot_channel(server_id, str(interaction.channel_id))
    if not ok:
        await interaction.response.send_message(f"âŒ NÃ£o consegui salvar o canal: {err}", ephemeral=True)
        return
    await interaction.response.send_message(
        "âœ… Pronto. A partir de agora, o modo chat (dizer **ola**) sÃ³ funciona neste canal.",
        ephemeral=True,
    )

@bot.tree.command(name="setup", description="Gera uma chave e configura o botÃ£o padrÃ£o")
@app_commands.describe(botao="BotÃ£o padrÃ£o (1-12) que o chat vai atualizar quando vocÃª disser 'ola'")
async def setup(interaction: discord.Interaction, botao: int = 1):
    """Gera chave de conexÃ£o para um servidor e configura UX por chat"""
    server_id = str(interaction.guild.id)
    key = create_connection_key(server_id)

    ok, err = set_default_button(server_id, botao)
    if not ok:
        await interaction.response.send_message(f"âŒ {err}", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="ðŸ”‘ Chave de ConexÃ£o Gerada",
        description=f"Copie esta chave e use no SminDeck",
        color=discord.Color.green()
    )
    embed.add_field(name="Sua Chave:", value=f"`{key}`", inline=False)
    embed.add_field(
        name="Como usar:",
        value=(
            "1. Abra o SminDeck e cole a chave nas configuraÃ§Ãµes\n"
            f"2. BotÃ£o padrÃ£o do chat: **{botao}**\n"
            "3. No canal do servidor, diga **ola** e eu vou pedir sÃ³ a URL"
        ),
        inline=False,
    )
    embed.set_footer(text="Mantenha essa chave segura!")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)
    print(f"ðŸ”‘ Chave criada para servidor: {server_id} - Chave: {key}")


@bot.tree.command(name="botao", description="Define qual botÃ£o o fluxo do chat (ola) vai atualizar")
@app_commands.describe(numero="BotÃ£o padrÃ£o (1-12)")
async def set_button(interaction: discord.Interaction, numero: int):
    server_id = str(interaction.guild.id)
    ok, err = set_default_button(server_id, numero)
    if not ok:
        await interaction.response.send_message(f"âŒ {err}", ephemeral=True)
        return
    await interaction.response.send_message(
        f"âœ… Pronto. Agora quando alguÃ©m disser **ola**, vou pedir a URL e atualizar o **BotÃ£o {numero}**.",
        ephemeral=True,
    )

@bot.tree.command(name="update-video", description="Atualiza URL de um vÃ­deo no SminDeck")
@app_commands.describe(
    chave="Sua chave de conexÃ£o com o SminDeck",
    botao="NÃºmero do botÃ£o (1-12)",
    url="URL do YouTube ou arquivo"
)
async def update_video(interaction: discord.Interaction, chave: str, botao: int, url: str):
    """Atualiza URL de um vÃ­deo"""
    
    # Validar entrada
    if not (1 <= botao <= 12):
        await interaction.response.send_message(
            "âŒ NÃºmero do botÃ£o deve estar entre 1 e 12",
            ephemeral=True
        )
        return
    
    if not url.startswith(('http://', 'https://')):
        await interaction.response.send_message(
            "âŒ URL deve comeÃ§ar com http:// ou https://",
            ephemeral=True
        )
        return
    
    # Atualizar URL no banco
    success, message = update_url(chave.strip().upper(), botao, url)
    
    if success:
        embed = discord.Embed(
            title="âœ… URL Atualizada!",
            description=f"BotÃ£o {botao} atualizado com sucesso",
            color=discord.Color.green()
        )
        embed.add_field(name="BotÃ£o:", value=str(botao), inline=True)
        embed.add_field(name="URL (primeiros 50 chars):", value=f"`{url[:50]}...`", inline=False)
        embed.set_footer(text="A mudanÃ§a serÃ¡ sincronizada no SminDeck em breve")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        print(f"âœ… URL atualizada - BotÃ£o: {botao}, Chave: {chave}")
    else:
        await interaction.response.send_message(
            f"âŒ Erro: {message}",
            ephemeral=True
        )

@bot.tree.command(name="listar-urls", description="Lista todas as URLs configuradas")
@app_commands.describe(chave="Sua chave de conexÃ£o com o SminDeck")
async def list_urls(interaction: discord.Interaction, chave: str):
    """Lista todas as URLs de uma chave"""
    urls = get_urls(chave.strip().upper())
    
    if not urls:
        await interaction.response.send_message(
            "â„¹ï¸ Nenhuma URL configurada ainda para essa chave",
            ephemeral=True
        )
        return
    
    embed = discord.Embed(
        title="ðŸ“º URLs Configuradas",
        description=f"Total: {len(urls)} URL(s)",
        color=discord.Color.blue()
    )
    
    for button, url in sorted(urls.items()):
        url_preview = url[:40] + "..." if len(url) > 40 else url
        embed.add_field(
            name=f"BotÃ£o {button}",
            value=f"`{url_preview}`",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="ajuda", description="Mostra como usar o bot")
async def help_command(interaction: discord.Interaction):
    """Mostra a ajuda"""
    embed = discord.Embed(
        title="ðŸ“– Ajuda - SminDeck Bot",
        description="Guia de como usar o bot Discord para controlar o SminDeck",
        color=discord.Color.gold()
    )
    
    embed.add_field(
        name="1ï¸âƒ£ /setup",
        value=(
            "Gera sua chave e define o botÃ£o padrÃ£o do chat\n"
            "Ex: `/setup botao:1`"
        ),
        inline=False
    )

    embed.add_field(
        name="âœ¨ Modo fÃ¡cil (chat)",
        value=(
            "No canal do servidor, diga **ola**.\n"
            "Eu vou pedir sÃ³ a URL e atualizar o botÃ£o padrÃ£o."
        ),
        inline=False
    )

    embed.add_field(
        name="2ï¸âƒ£ /botao",
        value="Define qual botÃ£o o modo fÃ¡cil vai atualizar\nEx: `/botao numero:3`",
        inline=False
    )
    
    embed.add_field(
        name="3ï¸âƒ£ /update-video (avanÃ§ado)",
        value="Atualiza a URL de um botÃ£o informando a chave\n`/update-video chave:ABC123 botao:1 url:https://youtube.com/...`",
        inline=False
    )
    
    embed.add_field(
        name="4ï¸âƒ£ /listar-urls",
        value="Lista todas as URLs configuradas\n`/listar-urls chave:ABC123`",
        inline=False
    )
    
    embed.add_field(
        name="ðŸ” SeguranÃ§a",
        value="â€¢ Mantenha sua chave segura\nâ€¢ Use em canais privados\nâ€¢ NÃ£o compartilhe com outros",
        inline=False
    )
    
    embed.set_footer(text="SminDeck Bot v1.0")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="debug", description="[Admin] Verifica chaves no banco")
async def debug_command(interaction: discord.Interaction):
    """Debug - mostra chaves no banco"""
    import sqlite3
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT server_id, connection_key FROM connection_keys")
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        await interaction.response.send_message("Nenhuma chave no banco", ephemeral=True)
        return
    
    msg = "**Chaves no banco:**\n"
    for server_id, key in results:
        msg += f"Server: {server_id} | Key: `{key}`\n"
    
    await interaction.response.send_message(msg, ephemeral=True)

# Executar bot@bot.command(name="criar-canal")
@commands.has_permissions(manage_channels=True)
async def criar_canal(ctx):
    """Comando para criar o canal #smindeck manualmente"""
    try:
        ch = await ensure_dedicated_channel(ctx.guild)
        if ch:
            await ctx.send(f"✅ Canal {ch.mention} está pronto!")
        else:
            await ctx.send("❌ Não consegui criar o canal. Verifique as permissões do bot.")
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ Não é possível iniciar o bot sem o DISCORD_TOKEN")
        exit(1)




