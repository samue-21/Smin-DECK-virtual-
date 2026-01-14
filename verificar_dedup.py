#!/usr/bin/env python3
import sqlite3, os, json

db = os.path.expanduser('~/.smindeckbot/smindeckbot.db')
conn = sqlite3.connect(db)
c = conn.cursor()

print('=== VERIFICANDO DEDUPLICAÇÃO ===\n')

c.execute('SELECT id, botao, tipo, dados, criada_em FROM atualizacoes ORDER BY botao, criada_em DESC')
rows = c.fetchall()

print(f'Total de registros: {len(rows)}\n')

for row in rows:
    id_r, botao, tipo, dados_j, criada_em = row
    dados = json.loads(dados_j)
    print(f'[ID:{id_r}] Bot:{botao} | Tipo:{tipo}')
    print(f'         Data: {criada_em}')
    print(f'         Dados: {dados}')
    print()

print('=== RESUMO POR BOTAO ===')
c.execute('''
    SELECT botao, COUNT(*) as total 
    FROM atualizacoes 
    GROUP BY botao 
    ORDER BY botao
''')

for botao, count in c.fetchall():
    status = '✓' if count == 1 else '❌ DUPLICADO'
    print(f'Botão {botao}: {count} registro(s) - {status}')

conn.close()
