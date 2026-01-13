#!/usr/bin/env python3
"""Corrige índices dos botões no VPS"""

import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect('72.60.244.240', username='root', password='sminbot2024', timeout=10)
    print('✅ Conectado ao VPS')
    
    # Verificar dados antes
    print('\n📊 Antes da atualização:')
    stdin, stdout, stderr = ssh.exec_command(
        "sqlite3 ~/.smindeckbot/smindeckbot.db 'SELECT botao, tipo, dados FROM atualizacoes;'"
    )
    print(stdout.read().decode())
    
    # Corrigir índice do botão de 6 para 5
    stdin, stdout, stderr = ssh.exec_command(
        "sqlite3 ~/.smindeckbot/smindeckbot.db 'UPDATE atualizacoes SET botao = 5 WHERE botao = 6;'"
    )
    print("✅ Comando UPDATE executado")
    
    time.sleep(1)
    
    # Verificar dados depois
    print('\n📊 Depois da atualização:')
    stdin, stdout, stderr = ssh.exec_command(
        "sqlite3 ~/.smindeckbot/smindeckbot.db 'SELECT botao, tipo, dados FROM atualizacoes;'"
    )
    print(stdout.read().decode())
    
    ssh.close()
    print('\n✅ Banco VPS atualizado com sucesso!')
    
except Exception as e:
    print(f'❌ Erro: {e}')
    import traceback
    traceback.print_exc()
