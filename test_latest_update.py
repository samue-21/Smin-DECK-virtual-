#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verifica se a última atualização foi registrada com o formato correto.
Se o bot enviou um arquivo corretamente, deve ter 'arquivo' e 'nome' keys.
"""

import json
import sys
import os

# Converter stdout para UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Tentar conectar ao banco e verificar última atualização
try:
    from database import obter_atualizacoes, listar_chaves_ativas
    
    print("=" * 70)
    print("VERIFICANDO ULTIMAS ATUALIZACOES DO BANCO")
    print("=" * 70)
    
    # Obter TODAS as atualizações (ordena por data descrescente)
    todas_atualizacoes = obter_atualizacoes()
    
    if not todas_atualizacoes:
        print("[!] Nenhuma atualizacao encontrada no banco!")
        sys.exit(0)
    
    # Pega as últimas 20 atualizações para análise
    ultimas = todas_atualizacoes[:20]
    
    print(f"\n[*] Total de atualizacoes: {len(todas_atualizacoes)}")
    print(f"[*] Analisando as ultimas {len(ultimas)} atualizacoes\n")
    print("-" * 70)
    
    corretas = 0
    erradas = 0
    desconhecidas = 0
    
    for i, att in enumerate(ultimas, 1):
        id_att, chave, tipo, botao, dados_str, criada_em = att
        
        # Parse JSON
        try:
            dados = json.loads(dados_str) if isinstance(dados_str, str) else dados_str
        except:
            dados = dados_str
        
        print(f"\n#{i} - ID: {id_att}")
        print(f"   [KEY] Chave: {chave[:15]}... | [TYPE] Tipo: {tipo:7} | [BTN] Botao: {botao}")
        print(f"   [TIME] Data: {criada_em}")
        print(f"   [DATA] Dados: ", end="")
        
        if isinstance(dados, dict):
            if 'arquivo' in dados:
                print("[OK] CORRETO!")
                print(f"      [FILE] arquivo: {dados.get('arquivo', '???')}")
                print(f"      [NAME] nome: {dados.get('nome', '???')}")
                if 'extraido_de' in dados:
                    print(f"      [ZIP] extraido_de: {dados.get('extraido_de', '???')}")
                corretas += 1
            elif 'conteudo' in dados:
                print("[ERRO] ERRADO (formato antigo)!")
                print(f"      [!] conteudo: {dados.get('conteudo', '???')}")
                erradas += 1
            else:
                print("[?] Formato desconhecido!")
                print(f"      {json.dumps(dados, ensure_ascii=True)}")
                desconhecidas += 1
        else:
            print("[?] Tipo desconhecido: {}".format(type(dados)))
            print(f"      {dados}")
            desconhecidas += 1
    
    print("\n" + "=" * 70)
    print("RESUMO:")
    print(f"   [OK] Corretas (com 'arquivo'): {corretas}/{len(ultimas)}")
    print(f"   [ERRO] Erradas (com 'conteudo'): {erradas}/{len(ultimas)}")
    print(f"   [?] Desconhecidas: {desconhecidas}/{len(ultimas)}")
    
    if erradas == 0 and desconhecidas == 0:
        print("\n[SUCCESS] Todas as atualizacoes estao no formato correto!")
    elif erradas > 0:
        print(f"\n[WARN] ATENCAO! {erradas} atualizacao(oes) ainda no formato antigo!")
    
    print("=" * 70)

except ImportError as e:
    print(f"[ERRO] Erro ao importar: {e}")
    print("Certifique-se de que voce esta no diretorio correto.")
    sys.exit(1)
except Exception as e:
    print(f"[ERRO] Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
