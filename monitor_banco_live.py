#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONITOR DO BANCO - Mostra em TEMPO REAL tudo que chega
"""

import sqlite3
import os
import time
import json
from datetime import datetime

DB_PATH = os.path.expanduser('~/.smindeckbot/smindeckbot.db')

def monitor_banco():
    print(f"\n{'='*80}")
    print(f"📊 MONITOR DO BANCO DE DADOS (tempo real)")
    print(f"{'='*80}\n")
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Banco não encontrado: {DB_PATH}")
        return
    
    count_anterior = -1
    ids_vistos = set()
    
    while True:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Pegar todas as atualizações
            cursor.execute('''
                SELECT id, chave, tipo, botao, dados, criada_em
                FROM atualizacoes
                ORDER BY criada_em DESC
            ''')
            
            rows = cursor.fetchall()
            count_atual = len(rows)
            conn.close()
            
            # Se novo arquivo chegou
            if count_atual > count_anterior:
                for row in rows:
                    id_reg, chave, tipo, botao, dados_json, criada_em = row
                    
                    if id_reg not in ids_vistos:
                        ids_vistos.add(id_reg)
                        dados = json.loads(dados_json)
                        
                        print(f"\n{'🟢 NOVO ARQUIVO CHEGOU!'}")
                        print(f"{'─'*80}")
                        print(f"⏰ {criada_em}")
                        print(f"📌 ID: {id_reg}")
                        print(f"🎯 Botão: {botao}")
                        print(f"📁 Tipo: {tipo}")
                        print(f"🔑 Chave: {chave[:25]}...")
                        print(f"\n📋 DADOS:")
                        for k, v in dados.items():
                            print(f"   • {k}: {v}")
                        
                        # Validar formato
                        tem_arquivo = 'arquivo' in dados
                        tem_nome = 'nome' in dados
                        tem_tamanho = 'tamanho' in dados
                        
                        print(f"\n✓ VALIDAÇÃO:")
                        print(f"   {'✓' if tem_arquivo else '✗'} arquivo: {dados.get('arquivo', 'FALTA!')}")
                        print(f"   {'✓' if tem_nome else '✗'} nome: {dados.get('nome', 'FALTA!')}")
                        print(f"   {'✓' if tem_tamanho else '✗'} tamanho: {dados.get('tamanho', 'FALTA!')}")
                        
                        if tem_arquivo and tem_nome and tem_tamanho:
                            print(f"\n✅ FORMATO CORRETO! Pronto para sincronizar.")
                        else:
                            print(f"\n❌ FORMATO INCORRETO! Faltam campos.")
                        
                        print(f"{'─'*80}\n")
                
                count_anterior = count_atual
            
            time.sleep(1)  # Verificar a cada 1 segundo
            
        except KeyboardInterrupt:
            print(f"\n\n{'='*80}")
            print(f"Monitor parado pelo usuário")
            print(f"{'='*80}\n")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
            time.sleep(2)

if __name__ == '__main__':
    monitor_banco()
