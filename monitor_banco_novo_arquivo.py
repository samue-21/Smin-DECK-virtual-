#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONITOR BANCO - Aguarda novo arquivo ser registrado
Execute ANTES de enviar arquivo via Discord!
"""

import json
import sys
import time
from datetime import datetime

try:
    from database import obter_atualizacoes
    
    print("="*70)
    print("[MONITOR] Aguardando novo arquivo ser registrado no banco...")
    print("="*70)
    print()
    print("Instruções:")
    print("  1. Este script está aguardando...")
    print("  2. Envie um arquivo via Discord bot")
    print("  3. Script detectará automaticamente quando chegar")
    print()
    print("="*70)
    print()
    
    inicial = len(obter_atualizacoes())
    inicio = time.time()
    timeout = 120
    
    while time.time() - inicio < timeout:
        todas = obter_atualizacoes()
        atual = len(todas)
        
        segundos = int(time.time() - inicio)
        
        if atual > inicial:
            print(f"\n[SUCESSO] Novo arquivo detectado!")
            print(f"Tempo: {segundos}s\n")
            print("="*70)
            
            # Mostra o novo arquivo
            att = todas[0]
            id_att, chave, tipo, botao, dados_str, criada_em = att
            
            try:
                dados = json.loads(dados_str)
            except:
                dados = dados_str
            
            print(f"\n[NOVO ARQUIVO REGISTRADO]")
            print(f"  ID: {id_att}")
            print(f"  Data: {criada_em}")
            print(f"  Tipo: {tipo}")
            print(f"  Botao: {botao}")
            print(f"  Chave: {chave[:20]}...")
            print(f"\n  Dados:")
            print(json.dumps(dados, ensure_ascii=False, indent=4))
            
            # Validações
            print(f"\n{'='*70}")
            print("[VALIDACOES]")
            print(f"{'='*70}\n")
            
            checks = []
            
            if isinstance(dados, dict):
                # Validar 'arquivo'
                if 'arquivo' in dados:
                    print(f"[OK] arquivo: {dados['arquivo']}")
                    checks.append(True)
                else:
                    print(f"[ERRO] arquivo ausente!")
                    checks.append(False)
                
                # Validar 'nome'
                if 'nome' in dados:
                    print(f"[OK] nome: {dados['nome']}")
                    checks.append(True)
                else:
                    print(f"[ERRO] nome ausente!")
                    checks.append(False)
                
                # Validar 'tamanho'
                if 'tamanho' in dados:
                    print(f"[OK] tamanho: {dados['tamanho']}MB")
                    checks.append(True)
                else:
                    print(f"[AVISO] tamanho ausente!")
                    checks.append(False)
            
            total_ok = sum(checks)
            print(f"\n{'='*70}")
            print(f"Validacoes: {total_ok}/{len(checks)} OK")
            print(f"{'='*70}\n")
            
            if total_ok == len(checks):
                print("[SUCCESS] TUDO ESTÁ CORRETO NO BANCO!")
            else:
                print("[AVISO] Alguns dados faltam!")
            
            sys.exit(0)
        
        print(f"\r[AGUARDANDO] {segundos}s... (Ctrl+C para sair)", end='', flush=True)
        time.sleep(1)
    
    print(f"\n\n[TIMEOUT] Nenhum arquivo foi registrado em {timeout}s!")
    print("Verifique se bot está rodando e se arquivo foi enviado!")
    sys.exit(1)
    
except Exception as e:
    print(f"[ERRO] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
