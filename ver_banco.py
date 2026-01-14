#!/usr/bin/env python3
import sqlite3, os, json

db = os.path.expanduser('~/.smindeckbot/smindeckbot.db')
conn = sqlite3.connect(db)
c = conn.cursor()

c.execute('SELECT COUNT(*) FROM atualizacoes')
count = c.fetchone()[0]
print(f'Total de atualizacoes: {count}')

if count > 0:
    c.execute('SELECT id, botao, tipo, dados, criada_em FROM atualizacoes ORDER BY criada_em DESC LIMIT 1')
    row = c.fetchone()
    id_r, botao, tipo, dados_j, criada_em = row
    dados = json.loads(dados_j)
    print(f'\n[ULTIMO ARQUIVO]')
    print(f'ID: {id_r}')
    print(f'Botao: {botao}')
    print(f'Tipo: {tipo}')
    print(f'Criado: {criada_em}')
    print(f'Dados:')
    for k, v in dados.items():
        print(f'  {k}: {v}')

conn.close()
