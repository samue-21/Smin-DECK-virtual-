#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEBUG - Mostra TUDO que está no banco de dados agora
"""

import json
import sys

try:
    from database import obter_atualizacoes
    
    print("="*70)
    print("DADOS NO BANCO DE DADOS - AGORA")
    print("="*70)
    print()
    
    todas = obter_atualizacoes()
    
    if not todas:
        print("[!] BANCO ESTÁ VAZIO!")
        print()
        print("Possíveis motivos:")
        print("  1. Bot não está rodando")
        print("  2. Bot não recebeu mensagens ainda")
        print("  3. Arquivo não foi enviado via Discord")
        print()
        print("Para debugar:")
        print("  1. Verifique se bot.py está rodando")
        print("  2. Verifique logs do bot")
        print("  3. Envie arquivo novamente via Discord")
        sys.exit(1)
    
    print(f"[TOTAL] {len(todas)} atualizacoes no banco\n")
    print("="*70)
    print()
    
    for i, att in enumerate(todas[:10], 1):
        id_att, chave, tipo, botao, dados_str, criada_em = att
        
        try:
            dados = json.loads(dados_str)
        except:
            dados = dados_str
        
        print(f"[#{i}]")
        print(f"  ID: {id_att}")
        print(f"  Data: {criada_em}")
        print(f"  Chave: {chave[:25]}...")
        print(f"  Tipo: {tipo}")
        print(f"  Botao: {botao}")
        print(f"  Dados: {json.dumps(dados, ensure_ascii=False, indent=4)}")
        print()
        print("-"*70)
        print()
    
    print("\n[OK] Banco contém dados!")
    
except Exception as e:
    print(f"[ERRO] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
