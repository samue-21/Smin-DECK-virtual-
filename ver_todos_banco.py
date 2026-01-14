#!/usr/bin/env python3
import sqlite3, os, json

db = os.path.expanduser('~/.smindeckbot/smindeckbot.db')
conn = sqlite3.connect(db)
c = conn.cursor()

c.execute('SELECT COUNT(*) FROM atualizacoes')
count = c.fetchone()[0]
print(f'Total de atualizacoes: {count}\n')

c.execute('SELECT id, botao, tipo, dados, criada_em FROM atualizacoes ORDER BY criada_em DESC')
for row in c.fetchall():
    id_r, botao, tipo, dados_j, criada_em = row
    dados = json.loads(dados_j)
    print(f'[{id_r}] Botão {botao} | Tipo: {tipo} | {criada_em}')
    print(f'    Dados:')
    for k, v in dados.items():
        print(f'      • {k}: {v}')
    
    # Validar formato
    tem_arquivo = 'arquivo' in dados
    tem_nome = 'nome' in dados
    tem_tamanho = 'tamanho' in dados
    status = '✓' if (tem_arquivo and tem_nome and tem_tamanho) else '✗'
    print(f'    Status: {status} (arquivo:{tem_arquivo}, nome:{tem_nome}, tamanho:{tem_tamanho})')
    print()

conn.close()
