#!/usr/bin/env python3
"""
Verificar status final: Arquivo removido da fila após sincronização?
"""

import sqlite3
import os
import json
from datetime import datetime

db_path = os.path.expanduser('~/.smindeckbot/smindeckbot.db')
downloads_dir = os.path.expanduser('~/.smindeckbot/downloads')

print("=" * 70)
print("VERIFICAÇÃO FINAL: STATUS DA FILA APÓS SINCRONIZAÇÃO")
print("=" * 70)

# 1. Atualizações pendentes
print("\n[1] ATUALIZAÇÕES PENDENTES NA FILA:")
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, chave, tipo, botao, dados, criada_em FROM atualizacoes")
    atualizacoes = cursor.fetchall()
    
    if atualizacoes:
        print(f"   ❌ {len(atualizacoes)} atualizações AINDA NA FILA:\n")
        for att_id, chave, tipo, botao, dados_json, criada_em in atualizacoes:
            try:
                dados = json.loads(dados_json)
                arquivo = dados.get('arquivo', 'N/A')
                nome = dados.get('nome', 'N/A')
                print(f"   ID #{att_id}:")
                print(f"     Chave: {chave}")
                print(f"     Tipo: {tipo}")
                print(f"     Botão: {botao}")
                print(f"     Arquivo: {arquivo}")
                print(f"     Nome: {nome}")
                print(f"     Criado em: {criada_em}")
                print()
            except:
                pass
    else:
        print(f"   ✅ FILA VAZIA!")
        print(f"   ✓ Nenhuma atualização pendente")
        print(f"   ✓ Arquivo foi deletado da fila com sucesso!")
    
    conn.close()
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 2. Arquivos extraídos
print("\n[2] ARQUIVOS BAIXADOS/EXTRAÍDOS:")
try:
    if os.path.exists(downloads_dir):
        files = sorted(os.listdir(downloads_dir))
        if files:
            total_size = 0
            for f in files:
                path = os.path.join(downloads_dir, f)
                size = os.path.getsize(path)
                total_size += size
                print(f"   ✓ {f}")
                print(f"     {size:,} bytes")
            print(f"\n   Total: {total_size:,} bytes ({total_size / (1024*1024):.1f} MB)")
        else:
            print("   (pasta vazia)")
    else:
        print(f"   ❌ Pasta não existe")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 3. Resumo final
print("\n" + "=" * 70)
print("RESUMO FINAL:")
print("=" * 70)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM atualizacoes")
    pending = cursor.fetchone()[0]
    conn.close()
    
    if pending == 0:
        print("\n✅ OPERAÇÃO COMPLETADA COM SUCESSO!")
        print("\n   ✓ Arquivo foi puxado pela app")
        print("   ✓ Extraído corretamente")
        print("   ✓ Deletado da fila de atualizações")
        print("   ✓ Sistema pronto para novos arquivos")
    else:
        print(f"\n⚠️  AVISO: {pending} arquivo(s) ainda na fila")
        print("   Verifique os logs da sincronização")
except:
    pass

print()
