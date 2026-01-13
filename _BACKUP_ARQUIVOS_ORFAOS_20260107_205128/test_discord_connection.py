#!/usr/bin/env python3
"""
Script para testar se o bot consegue fazer login no Discord
"""
import asyncio
import discord
from discord.ext import commands
import sys
import os
from dotenv import load_dotenv

# Forcar UTF-8 no Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    print("[!] DISCORD_TOKEN nao encontrado no .env")
    sys.exit(1)

print(f"[*] Token encontrado: {TOKEN[:20]}...")
print(f"[*] Testando conexao com Discord...")

intents = discord.Intents(guilds=True, guild_messages=True, message_content=True, members=False)
test_bot = commands.Bot(command_prefix='/', intents=intents)

@test_bot.event
async def on_ready():
    print(f"[+] Bot conectado como: {test_bot.user}")
    print(f"[+] Guilds: {len(test_bot.guilds)}")
    for guild in test_bot.guilds:
        print(f"    - {guild.name} ({guild.id})")
    await test_bot.close()

@test_bot.event  
async def on_error(event, *args, **kwargs):
    import traceback
    print(f"[-] Erro no evento {event}:")
    traceback.print_exc()

try:
    print("[*] Iniciando bot...")
    asyncio.run(test_bot.start(TOKEN))
except Exception as e:
    print(f"[-] Erro ao conectar: {e}")
    import traceback
    traceback.print_exc()
