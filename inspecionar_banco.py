#!/usr/bin/env python3
"""
Script para inspecionar o banco de dados do VPS
Verifica atualizações órfãs e arquivos não encontrados
"""

import sqlite3
import json
import os
from pathlib import Path

DB_PATH = os.path.expanduser('~/.smindeckbot/smindeckbot.db')
ARQUIVOS_DIR = os.path.expanduser('~/.smindeckbot/arquivos')

def inspecionar_banco():
    """Inspeciona o banco de dados e identifica problemas"""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Banco de dados não encontrado: {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 1. Verificar atualizações
        print("=" * 80)
        print("📋 ATUALIZAÇÕES REGISTRADAS NO BANCO")
        print("=" * 80)
        
        cursor.execute('''
            SELECT id, chave, tipo, botao, dados, criada_em 
            FROM atualizacoes 
            ORDER BY criada_em DESC
        ''')
        
        atualizacoes = cursor.fetchall()
        
        if not atualizacoes:
            print("✅ Nenhuma atualização registrada")
        else:
            print(f"Total de atualizações: {len(atualizacoes)}\n")
            
            orfaos = []
            
            for row in atualizacoes:
                id_atu, chave, tipo, botao, dados_json, criada_em = row
                dados = json.loads(dados_json)
                
                arquivo = dados.get('arquivo')
                nome = dados.get('nome')
                conteudo = dados.get('conteudo')
                
                print(f"ID: {id_atu}")
                print(f"  Chave: {chave[:4]}***")
                print(f"  Tipo: {tipo}")
                print(f"  Botão: {botao + 1}")
                print(f"  Nome: {nome or conteudo or 'N/A'}")
                
                # Verificar se o arquivo existe
                if arquivo:
                    arquivo_path = os.path.join(ARQUIVOS_DIR, arquivo)
                    existe = os.path.exists(arquivo_path)
                    status = "✅ EXISTE" if existe else "❌ NÃO ENCONTRADO"
                    print(f"  Arquivo: {arquivo} [{status}]")
                    
                    if not existe:
                        orfaos.append(id_atu)
                
                print()
        
        # 2. Verificar arquivos soltos
        print("=" * 80)
        print("📁 ARQUIVOS NO DISCO")
        print("=" * 80)
        
        if os.path.exists(ARQUIVOS_DIR):
            arquivos_disco = os.listdir(ARQUIVOS_DIR)
            print(f"Total de arquivos no disco: {len(arquivos_disco)}\n")
            
            # Listar alguns arquivos
            for arquivo in arquivos_disco[:20]:
                caminho = os.path.join(ARQUIVOS_DIR, arquivo)
                tamanho = os.path.getsize(caminho) / (1024 * 1024)
                print(f"  📄 {arquivo} ({tamanho:.1f}MB)")
            
            if len(arquivos_disco) > 20:
                print(f"  ... e mais {len(arquivos_disco) - 20} arquivos")
        else:
            print(f"❌ Diretório não encontrado: {ARQUIVOS_DIR}")
        
        # 3. Listar atualizações órfãs
        if orfaos:
            print("\n" + "=" * 80)
            print("⚠️  ATUALIZAÇÕES COM ARQUIVOS FALTANDO")
            print("=" * 80)
            print(f"IDs de atualizações órfãs: {orfaos}\n")
            
            print("🗑️  Removendo atualizações órfãs...")
            for id_orf in orfaos:
                cursor.execute('DELETE FROM atualizacoes WHERE id = ?', (id_orf,))
                print(f"  ✅ Removido ID: {id_orf}")
            
            conn.commit()
            print(f"\n✅ {len(orfaos)} atualização(ões) órfã(s) removida(s)")
        else:
            print("\n✅ Nenhuma atualização órfã encontrada")
        
        # 4. Resumo final
        print("\n" + "=" * 80)
        print("📊 RESUMO")
        print("=" * 80)
        
        cursor.execute('SELECT COUNT(*) FROM atualizacoes')
        count_atualizacoes = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM chaves_ativas')
        count_chaves = cursor.fetchone()[0]
        
        print(f"✅ Atualizações válidas: {count_atualizacoes}")
        print(f"✅ Chaves ativas: {count_chaves}")
        print(f"✅ Arquivos no disco: {len(os.listdir(ARQUIVOS_DIR)) if os.path.exists(ARQUIVOS_DIR) else 0}")
        
    finally:
        conn.close()

if __name__ == '__main__':
    print("🔍 INSPEÇÃO DO BANCO DE DADOS DO VPS\n")
    inspecionar_banco()
    print("\n✅ Inspeção concluída!")
