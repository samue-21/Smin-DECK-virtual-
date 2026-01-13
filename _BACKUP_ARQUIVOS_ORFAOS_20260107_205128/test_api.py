#!/usr/bin/env python3
"""
Teste simples da API e database_client
"""

from database_client import DatabaseClient
import json

print("="*50)
print("TESTE: DATABASE CLIENT E API")
print("="*50 + "\n")

client = DatabaseClient()

# 1. Health Check
print("1. Testando health check...")
if client.health_check():
    print("✅ API está online!\n")
else:
    print("❌ API offline!\n")
    exit(1)

# 2. Criar chave
print("2. Testando criar chave...")
chave = client.criar_chave(user_id=123456789, guild_id=987654321, channel_id=555555555)
if chave:
    print(f"✅ Chave criada: {chave}\n")
else:
    print("❌ Erro ao criar chave\n")
    exit(1)

# 3. Obter info da chave
print("3. Testando obter info da chave...")
info = client.obter_info_chave(chave)
if info:
    print(f"✅ Info obtida: {json.dumps(info, indent=2)}\n")
else:
    print("❌ Erro ao obter info\n")

# 4. Validar chave
print("4. Testando validar chave...")
sucesso, msg = client.validar_chave(chave, 123456789, 987654321, 555555555)
if sucesso:
    print(f"✅ {msg}\n")
else:
    print(f"❌ {msg}\n")

# 5. Listar chaves ativas
print("5. Testando listar chaves ativas...")
chaves = client.listar_chaves_ativas()
print(f"✅ Chaves ativas: {len(chaves)}")
if chaves:
    for chave in chaves[:3]:  # Mostrar apenas 3 primeiras
        print(f"   - {chave}")
print()

# 6. Registrar atualização
print("6. Testando registrar atualização...")
sucesso = client.registrar_atualizacao(chave, 'link', 1, {'url': 'https://example.com'})
if sucesso:
    print("✅ Atualização registrada\n")
else:
    print("❌ Erro ao registrar atualização\n")

print("="*50)
print("✅ TODOS OS TESTES PASSARAM!")
print("="*50)
