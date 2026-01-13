#!/usr/bin/env python3
"""
Verificar se arquivo foi removido da fila após sincronização bem-sucedida
"""

import sqlite3
import os
import json

db_path = os.path.expanduser('~/.smindeckbot/smindeckbot.db')
downloads_dir = os.path.expanduser('~/.smindeckbot/downloads')

print("=" * 70)
print("VERIFICAÇÃO: ARQUIVO REMOVIDO DA FILA?")
print("=" * 70)

# 1. Ver estado do banco de dados
print("\n[1] BANCO DE DADOS - Atualizações pendentes:")
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Ver todas as atualizações
    cursor.execute("SELECT id, bot_id, tipo, dados FROM atualizacoes")
    atualizacoes = cursor.fetchall()
    
    if atualizacoes:
        print(f"   ❌ ENCONTRADAS {len(atualizacoes)} atualizações pendentes!")
        for att_id, bot_id, tipo, dados_json in atualizacoes:
            try:
                dados = json.loads(dados_json)
                arquivo = dados.get('arquivo', 'N/A')
                print(f"\n   Atualização #{att_id}:")
                print(f"     Bot ID: {bot_id}")
                print(f"     Tipo: {tipo}")
                print(f"     Arquivo: {arquivo}")
            except:
                print(f"   Atualização #{att_id}: (erro ao parsear)")
    else:
        print(f"   ✅ FILA VAZIA! (0 atualizações pendentes)")
        print(f"   ✓ Arquivo foi deletado com sucesso da fila!")
    
    conn.close()
except Exception as e:
    print(f"   ❌ Erro ao acessar DB: {e}")

# 2. Ver sincronizações
print("\n[2] SINCRONIZAÇÕES:")
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, timestamp, resultado FROM sincronizacao ORDER BY id DESC LIMIT 5")
    sincronizacoes = cursor.fetchall()
    
    for sync_id, timestamp, resultado in sincronizacoes:
        print(f"   - #{sync_id} em {timestamp}")
        try:
            res = json.loads(resultado)
            if res.get('sucesso'):
                print(f"     ✅ Sucesso")
            else:
                print(f"     ❌ Falha")
        except:
            pass
    
    conn.close()
except Exception as e:
    print(f"   Erro: {e}")

# 3. Ver arquivos em downloads
print("\n[3] ARQUIVOS EM DOWNLOADS:")
if os.path.exists(downloads_dir):
    files = sorted(os.listdir(downloads_dir))
    if files:
        for f in files:
            path = os.path.join(downloads_dir, f)
            size = os.path.getsize(path)
            print(f"   - {f}: {size:,} bytes")
    else:
        print("   (pasta vazia)")
else:
    print(f"   ❌ Pasta não existe")

print("\n" + "=" * 70)
print("CONCLUSÃO:")
print("=" * 70)

# Verificar final
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM atualizacoes")
    count = cursor.fetchone()[0]
    conn.close()
    
    if count == 0:
        print("✅ SUCESSO! Arquivo foi completamente removido da fila após sincronização.")
        print("   A app puxou o arquivo com sucesso e o deletou da API.")
    else:
        print(f"⚠️  {count} arquivo(s) ainda na fila - verifique se houve erro na sincronização")
except:
    pass
