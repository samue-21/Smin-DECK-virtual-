#!/usr/bin/env python3
"""
Verificar tentativas de cada atualização
"""

import sqlite3
import os
import json

db_path = os.path.expanduser('~/.smindeckbot/smindeckbot.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 70)
print("STATUS DAS ATUALIZAÇÕES - TENTATIVAS E DADOS")
print("=" * 70)

# Ver todas as atualizações com detalhes
cursor.execute("""
    SELECT id, chave, tipo, botao, dados, tentativas, criada_em 
    FROM atualizacoes 
    ORDER BY tentativas DESC
""")

atualizacoes = cursor.fetchall()

print(f"\nTotal: {len(atualizacoes)} atualizações\n")

if atualizacoes:
    for att_id, chave, tipo, botao, dados_json, tentativas, criada_em in atualizacoes:
        print(f"[ID #{att_id}] TENTATIVAS: {tentativas}")
        print(f"  Chave: {chave}")
        print(f"  Tipo: {tipo}")
        print(f"  Botão: {botao}")
        print(f"  Criada em: {criada_em}")
        
        try:
            dados = json.loads(dados_json)
            if 'arquivo' in dados:
                print(f"  Arquivo: {dados.get('arquivo')}")
                print(f"  Nome: {dados.get('nome')}")
            else:
                print(f"  Conteúdo: {dados.get('conteudo', 'N/A')[:100]}")
        except:
            print(f"  Dados: (erro ao parsear)")
        
        print()
else:
    print("✅ Nenhuma atualização na fila")

conn.close()

# Verificar também limite de tentativas
print("\n" + "=" * 70)
print("NOTA: Limite de tentativas é 2")
print("=" * 70)
