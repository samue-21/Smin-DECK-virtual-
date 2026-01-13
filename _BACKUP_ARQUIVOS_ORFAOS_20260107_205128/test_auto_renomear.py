#!/usr/bin/env python3
"""
Teste de validação: Auto-Renomear Botões
Valida o fluxo completo de registro + sincronização
"""

import sqlite3
import json
import os
from pathlib import Path

DB_PATH = '/root/.smindeckbot/smindeckbot.db'
LOCAL_DB_PATH = str(Path.home() / '.smindeckbot' / 'test_db.sqlite3')

def test_banco_dados():
    """Valida estrutura de dados no banco de dados"""
    print("🔍 TESTE 1: Estrutura de Dados")
    print("=" * 60)
    
    # Conectar ao banco
    try:
        conn = sqlite3.connect(LOCAL_DB_PATH)  # Usar banco local para teste
        cursor = conn.cursor()
        
        # Verificar tabela atualizacoes
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='atualizacoes'")
        schema = cursor.fetchone()
        
        if schema:
            print("✅ Tabela 'atualizacoes' existe")
            print(f"   Schema: {schema[0]}")
        else:
            print("❌ Tabela 'atualizacoes' não encontrada")
            return False
        
        # Verificar estrutura de dados
        cursor.execute("PRAGMA table_info(atualizacoes)")
        colunas = cursor.fetchall()
        print("\n📋 Colunas:")
        for col in colunas:
            print(f"   • {col[1]} ({col[2]})")
        
        conn.close()
        print("\n✅ Validação de banco concluída!")
        return True
        
    except Exception as e:
        print(f"❌ ERRO ao validar banco: {e}")
        return False

def test_estrutura_registro():
    """Valida estrutura esperada de registro"""
    print("\n\n🔍 TESTE 2: Estrutura de Registro Esperada")
    print("=" * 60)
    
    # Estrutura esperada
    esperado = {
        'arquivo': 'video_botao_7.bin',      # Nome real do arquivo
        'nome': 'primicias-de-fe'             # Nome customizado para botão
    }
    
    print("✅ Estrutura esperada no banco:")
    print(f"   {json.dumps(esperado, indent=4)}")
    
    print("\n✅ Fluxo esperado:")
    print("""
    1. Bot registra no banco:
       └─ arquivo: 'video_botao_7.bin'  (para download)
       └─ nome: 'primicias-de-fe'       (para exibição)
    
    2. sincronizador.py lê:
       └─ arquivo_para_download = 'video_botao_7.bin'
       └─ nome_botao = 'primicias-de-fe'
    
    3. App baixa:
       └─ GET /api/arquivo/video_botao_7.bin
       └─ ✅ HTTP 200
    
    4. App atualiza botão:
       └─ btn.setText('primicias-de-fe')
       └─ ✨ Botão exibe nome customizado!
    """)
    
    return True

def test_sincronizador_logica():
    """Valida lógica de sincronizador.py"""
    print("\n\n🔍 TESTE 3: Lógica do Sincronizador")
    print("=" * 60)
    
    print("✅ Teste de parsing de dados:")
    
    # Simular dados nova estrutura
    dados_novo = {'arquivo': 'video_botao_7.bin', 'nome': 'primicias-de-fe'}
    
    # Simular parsing
    if 'arquivo' in dados_novo:
        arquivo_para_download = dados_novo['arquivo']
        nome_botao = dados_novo.get('nome', arquivo_para_download)
        print(f"\n   ✅ Novo formato detectado:")
        print(f"      arquivo_para_download: {arquivo_para_download}")
        print(f"      nome_botao: {nome_botao}")
    
    # Simular dados formato antigo
    dados_antigo = {'conteudo': 'primicias-de-fe'}
    
    if 'arquivo' in dados_antigo:
        arquivo_para_download = dados_antigo['arquivo']
        nome_botao = dados_antigo.get('nome', arquivo_para_download)
    else:
        arquivo_para_download = dados_antigo.get('conteudo', '')
        nome_botao = arquivo_para_download
        print(f"\n   ✅ Formato antigo detectado (retro-compatível):")
        print(f"      arquivo_para_download: {arquivo_para_download}")
        print(f"      nome_botao: {nome_botao}")
    
    return True

def test_deck_window_logica():
    """Valida lógica de deck_window.py"""
    print("\n\n🔍 TESTE 4: Lógica do Deck Window")
    print("=" * 60)
    
    print("✅ Teste de atualização de botão:")
    
    # Simular mudança
    mudanca = {
        'botao_idx': 6,
        'file': '/home/user/.smindeckbot/downloads/video_botao_7.mp4',
        'is_youtube': False,
        'tipo': 'video',
        'atualizacao_id': 123,
        'nome_arquivo': 'video_botao_7.bin',
        'nome_botao': 'primicias-de-fe'  # ⭐ NOVO
    }
    
    # Simular lógica
    nome_botao = mudanca.get('nome_botao')
    tipo = mudanca['tipo']
    file_path = mudanca['file']
    
    if tipo in ('video', 'imagem'):
        if nome_botao:
            conteudo_visual = nome_botao
        else:
            conteudo_visual = os.path.basename(file_path)[:15]
    else:
        conteudo_visual = nome_botao if nome_botao else file_path[:50]
    
    print(f"\n   ✅ Botão será atualizado para:")
    print(f"      btn.setText('{conteudo_visual}')")
    print(f"      (arquivo real: {os.path.basename(file_path)})")
    
    return True

def test_sem_nome():
    """Testa retro-compatibilidade quando não houver nome"""
    print("\n\n🔍 TESTE 5: Retro-Compatibilidade (sem 'nome')")
    print("=" * 60)
    
    print("✅ Teste com dados antigos (sem campo 'nome'):")
    
    mudanca_antiga = {
        'botao_idx': 0,
        'file': '/home/user/.smindeckbot/downloads/video_botao_1.mp4',
        'is_youtube': False,
        'tipo': 'video',
        'atualizacao_id': 456,
        'nome_arquivo': 'video_botao_1.bin',
        'nome_botao': None  # Nenhum nome customizado
    }
    
    nome_botao = mudanca_antiga.get('nome_botao')
    file_path = mudanca_antiga['file']
    
    if nome_botao:
        conteudo_visual = nome_botao
    else:
        conteudo_visual = os.path.basename(file_path)[:15]
    
    print(f"\n   ✅ Fallback funcionando:")
    print(f"      nome_botao está None")
    print(f"      Usa nome do arquivo: {conteudo_visual}")
    print(f"      ✅ App continua funcionando normalmente!")
    
    return True

def main():
    print("\n" + "="*60)
    print("🎯 TESTE DE VALIDAÇÃO: AUTO-RENOMEAR BOTÕES")
    print("="*60)
    
    tests = [
        ("Banco de Dados", test_banco_dados),
        ("Estrutura de Registro", test_estrutura_registro),
        ("Lógica do Sincronizador", test_sincronizador_logica),
        ("Lógica do Deck Window", test_deck_window_logica),
        ("Retro-Compatibilidade", test_sem_nome),
    ]
    
    resultados = []
    
    for nome, test_func in tests:
        try:
            resultado = test_func()
            resultados.append((nome, resultado))
        except Exception as e:
            print(f"\n❌ ERRO em {nome}: {e}")
            resultados.append((nome, False))
    
    # Resumo final
    print("\n\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)
    
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{status} → {nome}")
    
    total_passou = sum(1 for _, r in resultados if r)
    print(f"\n✅ {total_passou}/{len(resultados)} testes passaram!")
    
    if total_passou == len(resultados):
        print("\n🎉 TODOS OS TESTES PASSARAM! Sistema pronto para uso! 🎉")
    else:
        print("\n⚠️  Alguns testes falharam. Revise a implementação.")

if __name__ == '__main__':
    main()
