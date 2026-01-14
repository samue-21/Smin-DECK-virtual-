#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TESTE CRÍTICO: Verificar se arquivo sobe para o banco

Passos esperados:
1. Você envia arquivo para discord (ex: Botão 9, tipo: video, arquivo: 143MB)
2. Bot pede seu nome customizado (ex: "teste 3")
3. Bot processa arquivo
4. CONSOLE mostra logs [1] até [34]
5. BANCO DE DADOS recebe atualização com dados corretos
6. App sincroniza

Se arquivo NÃO aparecer no banco:
- Veja qual log aparece POR ÚLTIMO na console (ex: [27], [28], etc)
- Isso indica onde o processo parou
"""

import sqlite3
import os
import time
import json
from pathlib import Path

DB_PATH = os.path.expanduser('~/.smindeckbot/smindeckbot.db')

def mostrar_estado_banco():
    """Mostra estado ATUAL do banco"""
    if not os.path.exists(DB_PATH):
        print("❌ Banco não existe!")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Total de atualizações
    cursor.execute('SELECT COUNT(*) FROM atualizacoes')
    total = cursor.fetchone()[0]
    
    print(f"\n{'='*70}")
    print(f"📊 ESTADO ATUAL DO BANCO")
    print(f"{'='*70}")
    print(f"Total de atualizações: {total}")
    
    if total > 0:
        # Mostrar últimas 3 atualizações
        cursor.execute('''
            SELECT id, chave, tipo, botao, dados, criada_em
            FROM atualizacoes
            ORDER BY criada_em DESC
            LIMIT 3
        ''')
        
        print(f"\nÚltimas 3 atualizações:")
        for row in cursor.fetchall():
            id_reg, chave, tipo, botao, dados_json, criada_em = row
            dados = json.loads(dados_json)
            
            print(f"\n[{id_reg}] Botão {botao} | Tipo: {tipo}")
            print(f"    Chave: {chave[:20]}...")
            print(f"    Dados: {dados}")
            print(f"    Criado: {criada_em}")
    
    conn.close()


def aguardar_novo_arquivo():
    """Monitora banco esperando novo arquivo"""
    print(f"\n{'='*70}")
    print(f"⏳ MONITORANDO BANCO...")
    print(f"{'='*70}")
    print(f"\nEnvie o arquivo para Discord AGORA!")
    print(f"Aguardando por 120 segundos...\n")
    
    # Pegar count inicial
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM atualizacoes')
    count_inicial = cursor.fetchone()[0]
    conn.close()
    
    inicio = time.time()
    while time.time() - inicio < 120:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM atualizacoes')
        count_atual = cursor.fetchone()[0]
        
        if count_atual > count_inicial:
            # NOVO ARQUIVO ADICIONADO!
            print(f"\n✅ NOVO ARQUIVO DETECTADO!")
            
            # Pegar últimas informações
            cursor.execute('''
                SELECT id, chave, tipo, botao, dados, criada_em
                FROM atualizacoes
                ORDER BY criada_em DESC
                LIMIT 1
            ''')
            
            row = cursor.fetchone()
            if row:
                id_reg, chave, tipo, botao, dados_json, criada_em = row
                dados = json.loads(dados_json)
                
                print(f"\n{'='*70}")
                print(f"📥 ARQUIVO RECEBIDO NO BANCO")
                print(f"{'='*70}")
                print(f"ID: {id_reg}")
                print(f"Botão: {botao}")
                print(f"Tipo: {tipo}")
                print(f"Chave: {chave[:30]}...")
                print(f"Criado em: {criada_em}")
                print(f"\n📋 DADOS REGISTRADOS:")
                print(json.dumps(dados, indent=2, ensure_ascii=False))
                
                # Validar formato
                print(f"\n{'='*70}")
                print(f"✓ VALIDAÇÃO DE FORMATO")
                print(f"{'='*70}")
                
                tem_arquivo = 'arquivo' in dados
                tem_nome = 'nome' in dados
                tem_tamanho = 'tamanho' in dados
                
                arquivo_str = f"({dados.get('arquivo')})" if tem_arquivo else "❌"
                nome_str = f"({dados.get('nome')})" if tem_nome else "❌"
                tamanho_str = f"({dados.get('tamanho')}MB)" if tem_tamanho else "❌"
                
                print(f"✓ Tem 'arquivo': {tem_arquivo} {arquivo_str}")
                print(f"✓ Tem 'nome': {tem_nome} {nome_str}")
                print(f"✓ Tem 'tamanho': {tem_tamanho} {tamanho_str}")
                
                if tem_arquivo and tem_nome and tem_tamanho:
                    print(f"\n✅ FORMATO CORRETO! Arquivo pronto para sincronização.")
                else:
                    print(f"\n❌ FORMATO INCORRETO! Faltam campos.")
            
            conn.close()
            return True
        
        conn.close()
        time.sleep(2)  # Verificar a cada 2 segundos
    
    print(f"\n⏱️ TIMEOUT! Nenhum arquivo adicionado nos últimos 120 segundos.")
    print(f"Verifique:")
    print(f"  1. Console do bot - qual foi o ÚLTIMO log [X] que apareceu?")
    print(f"  2. Se recebeu erro 'Chave não encontrada'")
    print(f"  3. Se arquivo foi processado corretamente")
    return False


def main():
    print(f"\n{'='*70}")
    print(f"🔍 TESTE CRÍTICO - ARQUIVO SOBE PARA BANCO?")
    print(f"{'='*70}")
    
    # Mostrar estado inicial
    print(f"\n📍 Estado ANTES do envio:")
    mostrar_estado_banco()
    
    # Aguardar novo arquivo
    resultado = aguardar_novo_arquivo()
    
    # Mostrar estado final
    print(f"\n📍 Estado DEPOIS do envio:")
    mostrar_estado_banco()
    
    if resultado:
        print(f"\n✅ SUCESSO! Arquivo foi registrado no banco.")
        print(f"Próxima etapa: Verificar se App sincroniza.")
    else:
        print(f"\n❌ FALHA! Arquivo NÃO foi registrado.")
        print(f"Verifique os logs do bot para saber onde parou.")
    
    print(f"\n{'='*70}\n")


if __name__ == '__main__':
    main()
