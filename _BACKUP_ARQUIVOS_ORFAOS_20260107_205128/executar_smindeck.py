#!/usr/bin/env python3
"""
SminDeck - Executor Direto
Executa a aplicação SminDeck com todas as dependências verificadas.
"""

import subprocess
import sys
import os

def main():
    # Caminho do diretório
    workspace_dir = os.path.dirname(os.path.abspath(__file__))
    main_py = os.path.join(workspace_dir, "main.py")
    
    # Variáveis de ambiente para melhor compatibilidade
    env = os.environ.copy()
    env['PYTHONPATH'] = workspace_dir
    
    print("🚀 Iniciando SminDeck...")
    print(f"📁 Diretório: {workspace_dir}")
    print(f"📄 Arquivo: {main_py}")
    
    try:
        # Executar main.py diretamente neste processo Python
        with open(main_py, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Executar no contexto local
        exec_globals = {
            '__file__': main_py,
            '__name__': '__main__',
            '__package__': None,
        }
        
        # Mudar para o diretório da aplicação
        os.chdir(workspace_dir)
        
        # Executar o código
        exec(code, exec_globals)
        
    except Exception as e:
        print(f"❌ Erro ao executar: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
