#!/usr/bin/env python3
"""
Verificar as 3 atualizações que estão na fila
"""

import sqlite3
import os
import json

db_path = os.path.expanduser('~/.smindeckbot/smindeckbot.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 70)
print("ATUALIZAÇÕES NA FILA")
print("=" * 70)

# Ver atualizações
cursor.execute("SELECT id, chave, tipo, botao, dados, tentativas, criada_em FROM atualizacoes")
atualizacoes = cursor.fetchall()

print(f"\nTotal: {len(atualizacoes)} atualizações\n")

if atualizacoes:
    for att_id, chave, tipo, botao, dados_json, tentativas, criada_em in atualizacoes:
        print(f"ID #{att_id}:")
        print(f"  Chave: {chave}")
        print(f"  Tipo: {tipo}")
        print(f"  Botão: {botao}")
        print(f"  Tentativas: {tentativas}")
        print(f"  Criada em: {criada_em}")
        
        try:
            dados = json.loads(dados_json)
            arquivo = dados.get('arquivo', dados.get('conteudo', 'N/A'))
            nome = dados.get('nome', 'N/A')
            print(f"  Arquivo: {arquivo}")
            print(f"  Nome: {nome}")
        except:
            print(f"  Dados: {dados_json[:100]}...")
        
        print()

conn.close()
