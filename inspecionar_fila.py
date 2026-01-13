#!/usr/bin/env python3
"""
Script para inspecionar a fila de atualizacoes
Mostra: total, status de tentativas, detalhes
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.expanduser('~/.smindeckbot/smindeckbot.db')

def inspecionar_fila():
    """Inspecionar fila completa"""
    if not os.path.exists(DB_PATH):
        print(f"[ERRO] Banco de dados nao encontrado: {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Verificar estrutura da tabela
    cursor.execute("PRAGMA table_info(atualizacoes)")
    colunas = cursor.fetchall()
    
    print("="*80)
    print("[SCHEMA] Tabela atualizacoes")
    print("="*80)
    for col in colunas:
        print(f"  {col[1]}: {col[2]}")
    
    # Contar total
    cursor.execute("SELECT COUNT(*) FROM atualizacoes")
    total = cursor.fetchone()[0]
    
    print(f"\n[TOTAL] {total} atualizacoes na fila\n")
    
    # Listar todas com detalhes
    cursor.execute("""
        SELECT id, botao_idx, tipo, tentativas, criado_em, status 
        FROM atualizacoes 
        ORDER BY id DESC
    """)
    
    atualizacoes = cursor.fetchall()
    
    print("="*80)
    print("[FILA COMPLETA]")
    print("="*80)
    
    for idx, (id_att, botao_idx, tipo, tentativas, criado_em, status) in enumerate(atualizacoes, 1):
        print(f"\n[{idx}] ID={id_att} | Bot={botao_idx} | Tipo={tipo}")
        print(f"    Tentativas: {tentativas}/2 | Status: {status} | Criado: {criado_em}")
        
        # Marcar para limpeza se tentativas >= 2
        if tentativas >= 2:
            print(f"    ⚠️  PENDENTE DE LIMPEZA (tentativas: {tentativas})")
    
    # Resumo por status
    print("\n" + "="*80)
    print("[RESUMO POR STATUS]")
    print("="*80)
    
    cursor.execute("""
        SELECT status, COUNT(*) as total 
        FROM atualizacoes 
        GROUP BY status
    """)
    
    resumo = cursor.fetchall()
    for status_name, count in resumo:
        print(f"  {status_name}: {count}")
    
    # Verificar pendentes de limpeza
    cursor.execute("""
        SELECT id, botao_idx, tipo, tentativas 
        FROM atualizacoes 
        WHERE tentativas >= 2
    """)
    
    pendentes = cursor.fetchall()
    
    print("\n" + "="*80)
    print("[LIMPEZA NECESSARIA]")
    print("="*80)
    
    if pendentes:
        print(f"\n⚠️  {len(pendentes)} atualizacoes com >= 2 tentativas:\n")
        for id_att, botao_idx, tipo, tentativas in pendentes:
            print(f"  ID={id_att} | Bot={botao_idx} | Tipo={tipo} | Tentativas={tentativas}")
    else:
        print("\n✅ Nenhuma atualizacao com >= 2 tentativas")
    
    conn.close()

if __name__ == '__main__':
    inspecionar_fila()
