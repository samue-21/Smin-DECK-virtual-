#!/usr/bin/env python3
import sqlite3, os, json, time

db = os.path.expanduser('~/.smindeckbot/smindeckbot.db')

print("🔍 Monitorando banco... (Ctrl+C para parar)\n")

count_anterior = -1
while True:
    conn = sqlite3.connect(db)
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM atualizacoes')
    count = c.fetchone()[0]
    
    if count != count_anterior:
        print(f"[{time.strftime('%H:%M:%S')}] Total: {count} arquivo(s)")
        
        if count > 0:
            c.execute('SELECT id, botao, tipo, dados FROM atualizacoes ORDER BY criada_em DESC LIMIT 1')
            row = c.fetchone()
            if row:
                id_r, botao, tipo, dados_j = row
                dados = json.loads(dados_j)
                print(f"  • Botão {botao} | Tipo: {tipo}")
                print(f"  • Dados: {dados}")
        
        count_anterior = count
    
    conn.close()
    time.sleep(1)
