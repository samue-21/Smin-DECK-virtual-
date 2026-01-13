#!/usr/bin/env python3
"""
Script para testar a extração do arquivo ZIP do botão 8
Simula o fluxo completo: download → extração → validação
"""

import os
import sys
import json
from pathlib import Path

# Configurações
DOWNLOADS_DIR = os.path.expanduser('~/.smindeckbot/downloads')
DB_PATH = os.path.expanduser('~/.smindeckbot/data.db')

print("=" * 60)
print("TESTE DE EXTRAÇÃO - BOTÃO 8")
print("=" * 60)

# 1. Ver atualizações na fila
print("\n[1] Verificando fila de atualizações...")
try:
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Buscar todas as atualizações
    cursor.execute("SELECT id, bot_id, tipo, dados FROM atualizacoes ORDER BY id DESC LIMIT 10")
    atualizacoes = cursor.fetchall()
    
    if atualizacoes:
        for att_id, bot_id, tipo, dados_json in atualizacoes:
            try:
                dados = json.loads(dados_json)
                print(f"\nAtualização #{att_id}:")
                print(f"  Bot ID: {bot_id}")
                print(f"  Tipo: {tipo}")
                print(f"  Dados: {dados}")
            except:
                print(f"  Erro ao parsear dados JSON")
    else:
        print("  ℹ️  Nenhuma atualização encontrada")
    
    conn.close()
except Exception as e:
    print(f"  ❌ Erro: {e}")

# 2. Ver arquivos no downloads
print("\n[2] Arquivos no DOWNLOADS_DIR:")
try:
    if os.path.exists(DOWNLOADS_DIR):
        files = os.listdir(DOWNLOADS_DIR)
        if files:
            for f in sorted(files):
                file_path = os.path.join(DOWNLOADS_DIR, f)
                size = os.path.getsize(file_path)
                print(f"  - {f} ({size:,} bytes)")
        else:
            print("  (pasta vazia)")
    else:
        print(f"  ❌ Pasta não existe: {DOWNLOADS_DIR}")
except Exception as e:
    print(f"  ❌ Erro: {e}")

# 3. Testar extração
print("\n[3] Testando extração de arquivo ZIP...")

# Procurar por arquivo .zip ou .bin que pareça ser um ZIP
test_file = None
if os.path.exists(DOWNLOADS_DIR):
    for f in os.listdir(DOWNLOADS_DIR):
        file_path = os.path.join(DOWNLOADS_DIR, f)
        
        # Verificar magic bytes
        try:
            with open(file_path, 'rb') as fp:
                magic = fp.read(4)
                if magic == b'PK\x03\x04':  # ZIP magic bytes
                    test_file = file_path
                    print(f"  Encontrado arquivo ZIP: {f}")
                    break
        except:
            pass

if test_file:
    print(f"\n  Testando extração: {test_file}")
    
    # Tentar extrair usando sincronizador
    try:
        from sincronizador import extrair_arquivo_compactado_cliente
        
        # Tentar extrair como vídeo
        resultado = extrair_arquivo_compactado_cliente(test_file, 'video')
        
        if resultado:
            print(f"  ✅ Extração bem-sucedida!")
            print(f"  Arquivo extraído: {resultado}")
            print(f"  Existe? {os.path.exists(resultado)}")
            if os.path.exists(resultado):
                print(f"  Tamanho: {os.path.getsize(resultado):,} bytes")
        else:
            print(f"  ❌ Extração retornou None")
            
    except Exception as e:
        print(f"  ❌ Erro ao extrair: {e}")
        import traceback
        traceback.print_exc()
else:
    print("  ⚠️  Nenhum arquivo ZIP encontrado para testar")

# 4. Resumo
print("\n" + "=" * 60)
print("FIM DO TESTE")
print("=" * 60)
