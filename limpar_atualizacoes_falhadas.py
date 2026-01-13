#!/usr/bin/env python3
"""
Script de Limpeza Automática de Atualizações Falhadas
======================================================

Executado automaticamente quando uma atualização falha em 2 tentativas.
Remove:
1. A entrada da atualizacao do banco de dados
2. O arquivo da API (VPS)
3. Registra ação no log

Uso:
    python limpar_atualizacoes_falhadas.py --atualizacao_id <id> --tipo <tipo>
"""

import sys
import os
import argparse
import requests
from datetime import datetime
from pathlib import Path

# Adicionar diretório atual ao path
sys.path.insert(0, os.path.dirname(__file__))

from database import (
    deletar_atualizacao, 
    obter_atualizacoes_falhadas,
    DB_PATH
)

API_URL = 'http://72.60.244.240:5001'
DOWNLOADS_DIR = os.path.expanduser('~/.smindeckbot/downloads')
LOG_LIMPEZA = os.path.expanduser('~/.smindeckbot/limpeza_atualizacoes.log')

# Garantir pasta de logs
os.makedirs(os.path.dirname(LOG_LIMPEZA), exist_ok=True)


def registrar_log(mensagem):
    """Registra mensagem em arquivo de log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {mensagem}"
    
    try:
        with open(LOG_LIMPEZA, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
        print(log_message)
    except Exception as e:
        print(f"[ERRO] Falha ao registrar log: {e}")


def deletar_arquivo_vps(filename: str) -> bool:
    """Deleta arquivo do VPS (API)"""
    try:
        url = f'{API_URL}/api/arquivo/{filename}'
        print(f"[LIMPEZA] DELETE: {url}")
        
        resp = requests.delete(url, timeout=10)
        if resp.status_code == 200:
            registrar_log(f"[DELETADO] VPS: {filename}")
            return True
        else:
            registrar_log(f"[AVISO] Falha ao deletar do VPS: {filename} (status: {resp.status_code})")
            return False
    except Exception as e:
        registrar_log(f"[ERRO] Erro ao deletar do VPS: {filename} | {e}")
        return False


def deletar_arquivo_local(filename: str) -> bool:
    """Deleta arquivo do download local"""
    try:
        caminho = os.path.join(DOWNLOADS_DIR, filename)
        if os.path.exists(caminho):
            os.remove(caminho)
            registrar_log(f"[DELETADO] Local: {filename}")
            return True
        else:
            registrar_log(f"[AVISO] Arquivo local não encontrado: {filename}")
            return False
    except Exception as e:
        registrar_log(f"[ERRO] Erro ao deletar arquivo local: {filename} | {e}")
        return False


def limpar_atualizacao(atualizacao_id, tipo, dados):
    """Limpa uma atualização que falhou 2 vezes"""
    print(f"\n{'='*60}")
    print(f"INICIANDO LIMPEZA: Atualização #{atualizacao_id}")
    print(f"{'='*60}\n")
    
    registrar_log(f"{'='*60}")
    registrar_log(f"LIMPEZA INICIADA: Atualização #{atualizacao_id} (Tipo: {tipo})")
    registrar_log(f"{'='*60}")
    
    try:
        # Passo 1: Extrair nome do arquivo dos dados
        arquivo_nome = None
        if isinstance(dados, dict):
            arquivo_nome = dados.get('arquivo') or dados.get('conteudo')
        
        # Passo 2: Deletar arquivo do VPS
        if arquivo_nome and tipo in ('video', 'imagem', 'audio'):
            print(f"[1/3] Deletando arquivo do VPS: {arquivo_nome}")
            deletar_arquivo_vps(arquivo_nome)
        
        # Passo 3: Deletar arquivo local
        if arquivo_nome:
            print(f"[2/3] Deletando arquivo local: {arquivo_nome}")
            deletar_arquivo_local(arquivo_nome)
        
        # Passo 4: Deletar registro do banco de dados
        print(f"[3/3] Deletando do banco de dados...")
        sucesso = deletar_atualizacao(atualizacao_id)
        
        if sucesso:
            registrar_log(f"[OK] Atualizacao #{atualizacao_id} deletada do BD")
            registrar_log(f"[SUCESSO] Limpeza completa para atualizacao #{atualizacao_id}\n")
            
            print(f"\n[OK] LIMPEZA COMPLETA!")
            print(f"     - Arquivo VPS removido: {arquivo_nome}")
            print(f"     - Arquivo local removido")
            print(f"     - BD atualizado")
            return True
        else:
            registrar_log(f"[AVISO] Falha ao deletar de alguns componentes #{atualizacao_id}")
            return False
            
    except Exception as e:
        registrar_log(f"[ERRO] Erro durante limpeza: {e}")
        print(f"\n[ERRO] Falha na limpeza: {e}")
        return False


def limpar_atualizacoes_falhadas(max_tentativas=2):
    """Limpa todas as atualizações com mais de max_tentativas tentativas"""
    print(f"\n{'='*60}")
    print(f"VARREDURA DE ATUALIZACOES FALHADAS")
    print(f"{'='*60}\n")
    
    registrar_log(f"\n{'='*60}")
    registrar_log(f"VARREDURA: Procurando atualizacoes com >= {max_tentativas} tentativas")
    
    try:
        atualizacoes = obter_atualizacoes_falhadas(max_tentativas)
        
        if not atualizacoes:
            msg = f"Nenhuma atualizacao com >= {max_tentativas} tentativas encontrada"
            print(f"[INFO] {msg}")
            registrar_log(f"[INFO] {msg}")
            return 0
        
        print(f"[ENCONTRADAS] {len(atualizacoes)} atualizacao(oes) para limpeza\n")
        registrar_log(f"[ENCONTRADAS] {len(atualizacoes)} atualizacao(oes)")
        
        limpas = 0
        for atu in atualizacoes:
            if limpar_atualizacao(atu['id'], atu['tipo'], atu['dados']):
                limpas += 1
        
        msg = f"Limpeza finalizada: {limpas}/{len(atualizacoes)} atualizacoes removidas"
        print(f"\n[RESULTADO] {msg}")
        registrar_log(f"[RESULTADO] {msg}")
        
        return limpas
        
    except Exception as e:
        registrar_log(f"[ERRO] Erro durante varredura: {e}")
        print(f"[ERRO] Erro durante varredura: {e}")
        return 0


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Limpa atualizações que falharam 2 vezes'
    )
    parser.add_argument('--atualizacao_id', type=int, help='ID específico para limpeza')
    parser.add_argument('--tipo', type=str, help='Tipo de arquivo (video, imagem, etc)')
    parser.add_argument('--varredura', action='store_true', help='Varrer todas as falhadas')
    parser.add_argument('--max_tentativas', type=int, default=2, help='Max tentativas (padrão: 2)')
    
    args = parser.parse_args()
    
    print(f"[LIMPEZA] Iniciando script de limpeza automática")
    print(f"[BANCO] {DB_PATH}")
    print(f"[API] {API_URL}\n")
    
    try:
        if args.varredura:
            # Modo varredura: limpar todas as falhadas
            print(f"[MODO] Varredura completa de falhadas")
            limpar_atualizacoes_falhadas(args.max_tentativas)
            
        elif args.atualizacao_id:
            # Modo específico: limpar uma atualizacao
            print(f"[MODO] Limpeza específica: Atualizacao #{args.atualizacao_id}")
            
            # Ler dados do BD antes de deletar
            from database import obter_atualizacoes
            todas = obter_atualizacoes()
            
            atu_dados = None
            for a in todas:
                if a['id'] == args.atualizacao_id:
                    atu_dados = a
                    break
            
            if atu_dados:
                limpar_atualizacao(
                    args.atualizacao_id,
                    args.tipo or atu_dados['tipo'],
                    atu_dados['dados']
                )
            else:
                print(f"[AVISO] Atualizacao #{args.atualizacao_id} não encontrada no BD")
                registrar_log(f"[AVISO] Atualizacao #{args.atualizacao_id} não encontrada")
        else:
            # Modo padrão: varredura
            limpar_atualizacoes_falhadas(args.max_tentativas)
            
    except Exception as e:
        registrar_log(f"[ERRO] Erro fatal: {e}")
        print(f"[ERRO] Erro fatal: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
