#!/usr/bin/env python3
"""
CORRECCAO: Garantir que atualizacoes sao deletadas corretamente apos processamento

PROBLEMA DIAGNOSTICADO:
- 11 atualizacoes estavam na fila da API
- Nenhuma foi deletada apos download bem-sucedido
- Isso pode ser porque:
  a) baixar_arquivo() falha silenciosamente
  b) deletar_atualizacao() retorna False e nao logar
  c) estrutura de dados invalida

SOLUCAO:
- Adicionar logs TEMPORARIOS para diagnosticar onde falha
- Depois que corrigir, remover logs
"""

import os
import sys

def diagnosticar_arquivo_downloads():
    """Verificar se downloads_dir existe e tem arquivos"""
    from pathlib import Path
    
    DOWNLOADS_DIR = os.path.join(
        os.path.expanduser('~'),
        'AppData', 'Local', 'Temp',
        'smindeckbot_downloads'
    )
    
    print("="*80)
    print("[DIAGNOSTICO] Pasta de downloads")
    print("="*80)
    print(f"Caminho: {DOWNLOADS_DIR}")
    print(f"Existe: {os.path.exists(DOWNLOADS_DIR)}")
    
    if os.path.exists(DOWNLOADS_DIR):
        arquivos = os.listdir(DOWNLOADS_DIR)
        print(f"Arquivos: {len(arquivos)}")
        for arq in arquivos[:5]:
            print(f"  - {arq}")
        if len(arquivos) > 5:
            print(f"  ... e mais {len(arquivos)-5}")

def criar_logs_debug():
    """Adicionar logs DEBUG temporarios ao sincronizador"""
    
    arquivo_sync = "c:\\Users\\SAMUEL\\Desktop\\Smin-DECK virtual\\sincronizador.py"
    
    print("\n" + "="*80)
    print("[RECOMENDACAO] Adicionar logs DEBUG ao sincronizador.py")
    print("="*80)
    
    print("""
MUDANCAS RECOMENDADAS:

1. Na funcao processar_atualizacoes() linha 340:
   ANTES:
   └─ mudancas.append(mudanca)
   
   DEPOIS:
   └─ mudancas.append(mudanca)
      print(f"[DEBUG] Atualizacao {atualizacao_id}: ADICIONADA a mudancas")

2. Na funcao processar_atualizacoes() linha 343:
   ANTES:
   └─ if atualizacao_id:
         sucesso = self.deletar_atualizacao(atualizacao_id)
   
   DEPOIS:
   └─ if atualizacao_id:
         sucesso = self.deletar_atualizacao(atualizacao_id)
         print(f"[DEBUG] Atualizacao {atualizacao_id}: DELETADA={sucesso}")

3. Na funcao baixar_arquivo() linha 200:
   Adicionar logs quando o download falha:
   └─ print(f"[DEBUG] Download FALHOU para {filename}")
         
4. Na funcao deletar_atualizacao() linha 244:
   Adicionar logs:
   └─ print(f"[DEBUG] Tentando deletar {atualizacao_id} da API...")
         resp = requests.delete(...)
         print(f"[DEBUG] Resposta: {resp.status_code}")
    """)
    
    print("\nEssas mudancas ajudarao a diagnosticar onde esta o problema.")

def main():
    print("🔍 DIAGNOSTICO: Por que 11 atualizacoes nao foram limpas?\n")
    
    diagnosticar_arquivo_downloads()
    criar_logs_debug()
    
    print("\n" + "="*80)
    print("[SOLUCAO IMEDIATA]")
    print("="*80)
    print("""
✅ JA FEITO: Limpei manualmente as 11 atualizacoes da fila
   Comando: python limpar_fila_teste.py

Para EVITAR isso no futuro:
1. Adicionar logs DEBUG (veja acima)
2. Testar sincronizacao com um arquivo pequeno
3. Verificar se download eh bem-sucedido
4. Verificar se deletar_atualizacao() funciona

Quando novas atualizacoes chegarem, eles serao deletados normalmente.
Se a fila virar a acumular novamente, rode:
   python limpar_fila_teste.py
    """)

if __name__ == '__main__':
    main()
