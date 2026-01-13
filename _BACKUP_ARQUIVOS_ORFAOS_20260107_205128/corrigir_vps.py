#!/usr/bin/env python3
"""Conecta ao VPS e corrige índices dos botões"""

import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("Conectando ao VPS...")
    ssh.connect('72.60.244.240', username='root', password='sminbot2024', timeout=10)
    print("✅ Conectado!")
    
    # Executar comando SQL
    cmd = 'sqlite3 ~/.smindeckbot/smindeckbot.db "UPDATE atualizacoes SET botao = 5 WHERE botao = 6;"'
    print(f"Executando: {cmd}")
    
    stdin, stdout, stderr = ssh.exec_command(cmd)
    error = stderr.read().decode()
    
    if error:
        print(f"⚠️ Stderr: {error}")
    else:
        print("✅ UPDATE executado com sucesso")
    
    # Verificar resultado
    cmd2 = 'sqlite3 ~/.smindeckbot/smindeckbot.db "SELECT botao, tipo, conteudo FROM atualizacoes LIMIT 1;"'
    stdin, stdout, stderr = ssh.exec_command(cmd2)
    result = stdout.read().decode()
    print(f"Resultado: {result}")
    
    ssh.close()
    print("✅ Conexão fechada")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
