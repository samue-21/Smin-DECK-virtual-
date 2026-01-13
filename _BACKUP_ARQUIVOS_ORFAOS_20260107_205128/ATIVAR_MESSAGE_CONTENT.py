#!/usr/bin/env python3
"""
📋 INSTRUÇÕES PARA ATIVAR MESSAGE CONTENT INTENT NO DISCORD
================================

PASSO 1: Acesse o Discord Developer Portal
   → https://discord.com/developers/applications/

PASSO 2: Selecione seu bot (SminDeck)
   → Bot ID: 1457841504893538385

PASSO 3: Vá para a aba "Bot"
   → Na seção "TOKEN", você verá suas configurações

PASSO 4: Procure por "PRIVILEGED GATEWAY INTENTS" (logo abaixo do token)
   → Você vai ver 3 opções:
      ✓ Presence Intent
      ✓ Server Members Intent  
      ✓ Message Content Intent ← ATIVAR ESTA!

PASSO 5: Clique no toggle para ATIVAR "Message Content Intent"
   → Deve ficar AZUL/LIGADO

PASSO 6: Discord vai avisar que você precisa confirmar
   → Leia o aviso e confirme que entende

PASSO 7: Salve as mudanças (caso necessário)

PASSO 8: Após ativar, o bot será reiniciado automaticamente

================================
RESULTADO ESPERADO:
✅ Bot vai responder a mensagens e comandos
✅ Comandos / (slash commands) vão funcionar
✅ Não mais avisos sobre "message content intent is missing"

================================
SE NÃO CONSEGUIR ATIVAR:
- Verifique se você é o owner da aplicação Discord
- Seu bot pode estar em mais de 100 servidores (restrição do Discord)
- Nesse caso, precisa usar apenas Slash Commands (/)

================================
"""

print(__doc__)

import webbrowser
import time

print("\n🔗 Abrindo Discord Developer Portal...")
time.sleep(1)
webbrowser.open("https://discord.com/developers/applications/1457841504893538385/bot")
print("✅ Portal aberto no seu navegador!")
print("\n⏳ Após ativar a intent, execute: python gerenciar_bot.py restart")
