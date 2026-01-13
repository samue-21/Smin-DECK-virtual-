#!/usr/bin/env python3
"""
Teste de fluxo completo:
1. User envia "oi" no Discord
2. Bot cria chave no banco
3. User entra chave no APP
4. APP valida chave no banco
5. Bot vê que está autenticado e responde
"""

from database_client import DatabaseClient
import json
import time

print("="*60)
print("TESTE DE FLUXO COMPLETO")
print("="*60 + "\n")

client = DatabaseClient()

# Simular user Discord
DISCORD_USER_ID = 999666333
DISCORD_GUILD_ID = 888777666
DISCORD_CHANNEL_ID = 777666555

print(f"👤 User Discord ID: {DISCORD_USER_ID}")
print(f"🏰 Guild ID: {DISCORD_GUILD_ID}")
print(f"💬 Channel ID: {DISCORD_CHANNEL_ID}\n")

# PASSO 1: Bot recebe "oi" e cria chave
print("="*60)
print("PASSO 1: Bot cria chave (user enviou 'oi')")
print("="*60)

chave = client.criar_chave(DISCORD_USER_ID, DISCORD_GUILD_ID, DISCORD_CHANNEL_ID)
print(f"🔐 Chave gerada: {chave}\n")
time.sleep(1)

# PASSO 2: User copia chave e entra no APP
print("="*60)
print("PASSO 2: User entra chave no APP (tela de conexão bot)")
print("="*60)
print(f"User digitará: {chave}\n")
time.sleep(1)

# PASSO 3: APP valida chave no banco
print("="*60)
print("PASSO 3: APP valida chave via API")
print("="*60)

sucesso, msg = client.validar_chave(chave, DISCORD_USER_ID, DISCORD_GUILD_ID, DISCORD_CHANNEL_ID)
print(f"Resultado: {msg}\n")

if not sucesso:
    print("❌ Falha na validação!")
    exit(1)

time.sleep(1)

# PASSO 4: Verificar chaves ativas (via API remota)
print("="*60)
print("PASSO 4: Verificar chaves ativas no banco (via API)")
print("="*60)

ativas = client.listar_chaves_ativas()
print(f"✅ Total de chaves ativas: {len(ativas)}\n")

# Procurar a chave do user
user_encontrado = False
for ativa in ativas:
    if ativa['user_id'] == DISCORD_USER_ID:
        print(f"✅ User {DISCORD_USER_ID} encontrado nas chaves ativas!")
        print(f"   Chave: {ativa['chave']}")
        print(f"   Guild: {ativa['guild_id']}")
        print(f"   Channel: {ativa['channel_id']}\n")
        user_encontrado = True
        break

if not user_encontrado:
    print("❌ User não encontrado nas chaves ativas!")
    exit(1)

time.sleep(1)

# PASSO 5: App sincroniza updates
print("="*60)
print("PASSO 5: APP sincroniza atualizações")
print("="*60)

atualizacoes = client.obter_atualizacoes()
print(f"✅ Total de atualizações: {len(atualizacoes)}\n")

time.sleep(1)

# PASSO 6: Simular bot recebendo menu do user
print("="*60)
print("PASSO 6: User interage com menu (clica botão)")
print("="*60)

client.registrar_atualizacao(chave, 'link', 1, {'url': 'https://example.com', 'titulo': 'Novo Link'})
print("✅ Atualização registrada no banco\n")

print("="*60)
print("✅ TESTE COMPLETO COM SUCESSO!")
print("="*60)
print("""
RESUMO:
1. ✅ Bot criou chave
2. ✅ User copiou chave
3. ✅ APP validou chave via API
4. ✅ User aparece nas chaves ativas
5. ✅ APP sincronizou updates
6. ✅ User interagiu (registro de update)

🎉 FLUXO COMPLETO FUNCIONANDO!
""")
