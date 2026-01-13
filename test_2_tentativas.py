#!/usr/bin/env python3
"""
Test Suite: Sistema de 2 Tentativas com Limpeza Automática
===========================================================

Testa a integração entre:
- database.py (incrementar_tentativa, obter_tentativas)
- sincronizador.py (processar_atualizacoes com lógica de 2 tentativas)
- limpar_atualizacoes_falhadas.py (limpeza automática)
"""

import sys
import os
import sqlite3
import json
from pathlib import Path

# Adicionar diretório ao path
sys.path.insert(0, os.path.dirname(__file__))

from database import (
    init_database,
    registrar_atualizacao,
    incrementar_tentativa,
    obter_tentativas,
    obter_atualizacoes_falhadas,
    obter_atualizacoes,
    deletar_atualizacao,
    criar_chave,
    DB_PATH
)


def criar_chave_teste():
    """Cria uma chave de teste"""
    try:
        chave = criar_chave(user_id=123456, guild_id=789, channel_id=456)
        print(f"[OK] Chave de teste criada: {chave}")
        return chave
    except Exception as e:
        print(f"[ERRO] {e}")
        return None


def teste_incrementar_tentativa():
    """Testa incremento de tentativas"""
    print("\n" + "="*60)
    print("TESTE 1: Incrementar Tentativa")
    print("="*60 + "\n")
    
    # Criar chave
    chave = criar_chave_teste()
    if not chave:
        return False
    
    # Registrar atualização
    dados = {'arquivo': 'video_teste_1.bin', 'nome': 'teste-video-1'}
    registrar_atualizacao(chave, 'video', 0, dados)
    print("[OK] Atualização registrada")
    
    # Obter ID
    atualizacoes = obter_atualizacoes()
    atu_id = atualizacoes[0]['id'] if atualizacoes else None
    
    if not atu_id:
        print("[ERRO] Nenhuma atualização encontrada")
        return False
    
    print(f"[OK] ID da atualização: {atu_id}")
    
    # Teste 1: Incrementar para 1
    print("\n[TESTE] Incrementando para 1...")
    tentativa_1 = incrementar_tentativa(atu_id)
    assert tentativa_1 == 1, f"Esperado 1, obtido {tentativa_1}"
    print(f"[OK] Tentativa = {tentativa_1}")
    
    # Teste 2: Verificar obter_tentativas
    print("\n[TESTE] Verificando com obter_tentativas()...")
    tentativas = obter_tentativas(atu_id)
    assert tentativas == 1, f"Esperado 1, obtido {tentativas}"
    print(f"[OK] Tentativas = {tentativas}")
    
    # Teste 3: Incrementar para 2
    print("\n[TESTE] Incrementando para 2...")
    tentativa_2 = incrementar_tentativa(atu_id)
    assert tentativa_2 == 2, f"Esperado 2, obtido {tentativa_2}"
    print(f"[OK] Tentativa = {tentativa_2}")
    
    # Teste 4: Verificar novamente
    print("\n[TESTE] Verificando com obter_tentativas()...")
    tentativas = obter_tentativas(atu_id)
    assert tentativas == 2, f"Esperado 2, obtido {tentativas}"
    print(f"[OK] Tentativas = {tentativas}")
    
    # Limpar
    deletar_atualizacao(atu_id)
    print("\n[OK] Teste 1 PASSOU! ✅")
    return True


def teste_obter_atualizacoes_falhadas():
    """Testa obtenção de atualizações falhadas"""
    print("\n" + "="*60)
    print("TESTE 2: Obter Atualizações Falhadas")
    print("="*60 + "\n")
    
    # Criar múltiplas atualizações
    chave = criar_chave_teste()
    if not chave:
        return False
    
    # Atualization 1: Sem falhas (tentativas=0)
    registrar_atualizacao(chave, 'video', 0, {'arquivo': 'video_1.bin'})
    atualizacoes_1 = obter_atualizacoes()
    atu_id_1 = atualizacoes_1[0]['id']
    print(f"[OK] Atualização 1: {atu_id_1} (tentativas=0)")
    
    # Atualização 2: 1 falha
    registrar_atualizacao(chave, 'imagem', 1, {'arquivo': 'imagem_2.png'})
    atualizacoes_2 = obter_atualizacoes()
    atu_id_2 = atualizacoes_2[0]['id']
    incrementar_tentativa(atu_id_2)
    print(f"[OK] Atualização 2: {atu_id_2} (tentativas=1)")
    
    # Atualização 3: 2 falhas (deve aparecer em falhadas)
    registrar_atualizacao(chave, 'audio', 2, {'arquivo': 'audio_3.mp3'})
    atualizacoes_3 = obter_atualizacoes()
    atu_id_3 = atualizacoes_3[0]['id']
    incrementar_tentativa(atu_id_3)
    incrementar_tentativa(atu_id_3)
    print(f"[OK] Atualização 3: {atu_id_3} (tentativas=2)")
    
    # Teste: Obter falhadas
    print("\n[TESTE] Buscando atualizações com >= 2 tentativas...")
    falhadas = obter_atualizacoes_falhadas(max_tentativas=2)
    print(f"[OK] Encontradas {len(falhadas)} atualização(ões)")
    
    # Deve encontrar apenas a atualização 3
    assert len(falhadas) == 1, f"Esperado 1, encontrado {len(falhadas)}"
    assert falhadas[0]['id'] == atu_id_3, f"ID incorreto"
    print(f"[OK] ID correto: {falhadas[0]['id']}")
    print(f"[OK] Tipo correto: {falhadas[0]['tipo']}")
    print(f"[OK] Tentativas corretas: {falhadas[0]['tentativas']}")
    
    # Limpar
    deletar_atualizacao(atu_id_1)
    deletar_atualizacao(atu_id_2)
    deletar_atualizacao(atu_id_3)
    
    print("\n[OK] Teste 2 PASSOU! ✅")
    return True


def teste_fluxo_completo():
    """Testa fluxo completo de 2 tentativas"""
    print("\n" + "="*60)
    print("TESTE 3: Fluxo Completo (1a falha -> 2a falha -> Limpeza)")
    print("="*60 + "\n")
    
    # Criar chave e atualização
    chave = criar_chave_teste()
    if not chave:
        return False
    
    dados_originais = {'arquivo': 'video_teste_fluxo.bin', 'nome': 'teste-fluxo'}
    registrar_atualizacao(chave, 'video', 5, dados_originais)
    atualizacoes = obter_atualizacoes()
    atu_id = atualizacoes[0]['id']
    print(f"[OK] Atualização criada: {atu_id}")
    
    # Verificar estado inicial
    tentativas = obter_tentativas(atu_id)
    assert tentativas == 0, "Deveria começar com 0 tentativas"
    print(f"[OK] Estado inicial: tentativas=0")
    
    # Simular 1ª falha
    print("\n[SIMULACAO] 1ª tentativa falha...")
    tentativas = incrementar_tentativa(atu_id)
    assert tentativas == 1, f"Esperado 1, obtido {tentativas}"
    print(f"[OK] Após 1ª falha: tentativas={tentativas}")
    
    # Deve estar presente na fila (não foi removida)
    atualizacoes = obter_atualizacoes()
    ids = [a['id'] for a in atualizacoes]
    assert atu_id in ids, "Atualização deveria estar na fila após 1ª falha"
    print(f"[OK] Atualização ainda na fila (permite retry)")
    
    # Simular 2ª falha
    print("\n[SIMULACAO] 2ª tentativa falha...")
    tentativas = incrementar_tentativa(atu_id)
    assert tentativas == 2, f"Esperado 2, obtido {tentativas}"
    print(f"[OK] Após 2ª falha: tentativas={tentativas}")
    
    # Verificar que aparece em falhadas
    falhadas = obter_atualizacoes_falhadas(max_tentativas=2)
    ids_falhadas = [f['id'] for f in falhadas]
    assert atu_id in ids_falhadas, "Deveria aparecer em atualizações falhadas"
    print(f"[OK] Aparece em atualizações falhadas")
    
    # Simular limpeza
    print("\n[SIMULACAO] Executando limpeza automática...")
    sucesso = deletar_atualizacao(atu_id)
    assert sucesso, "Falha ao deletar atualização"
    print(f"[OK] Atualização removida do BD")
    
    # Verificar que foi removida
    atualizacoes = obter_atualizacoes()
    ids = [a['id'] for a in atualizacoes]
    assert atu_id not in ids, "Atualização deveria estar deletada"
    print(f"[OK] Atualização não está mais na fila")
    
    print("\n[OK] Teste 3 PASSOU! ✅")
    return True


def main():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("SUITE DE TESTES: 2 Tentativas com Limpeza Automática")
    print("="*60)
    
    try:
        # Inicializar BD
        init_database()
        print("[OK] Banco de dados inicializado")
        
        # Rodar testes
        testes = [
            ("Incrementar Tentativa", teste_incrementar_tentativa),
            ("Obter Atualizações Falhadas", teste_obter_atualizacoes_falhadas),
            ("Fluxo Completo", teste_fluxo_completo),
        ]
        
        resultados = []
        for nome, teste_func in testes:
            try:
                resultado = teste_func()
                resultados.append((nome, resultado))
            except AssertionError as e:
                print(f"\n[ERRO] {nome}: {e}")
                resultados.append((nome, False))
            except Exception as e:
                print(f"\n[ERRO] {nome}: {e}")
                import traceback
                traceback.print_exc()
                resultados.append((nome, False))
        
        # Resumo final
        print("\n" + "="*60)
        print("RESUMO DOS TESTES")
        print("="*60 + "\n")
        
        total = len(resultados)
        passados = sum(1 for _, r in resultados if r)
        
        for nome, resultado in resultados:
            status = "[OK] PASSOU" if resultado else "[ERRO] FALHOU"
            print(f"{status}: {nome}")
        
        print(f"\n[RESULTADO] {passados}/{total} testes passaram")
        
        if passados == total:
            print("\n[OK] TODOS OS TESTES PASSARAM!")
            return 0
        else:
            print(f"\n[AVISO] {total - passados} teste(s) falharam")
            return 1
            
    except Exception as e:
        print(f"\n[ERRO FATAL] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
