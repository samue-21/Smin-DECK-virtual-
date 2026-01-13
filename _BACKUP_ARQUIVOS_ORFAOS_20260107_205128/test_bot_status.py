#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar conectividade básica do bot
"""
import subprocess
import json
import sys
import io

# Forcar UTF-8
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("[*] Verificando se há processos do bot rodando...")

# Tentar pegar informações do VPS usando o deploy script
result = subprocess.run(
    ["python", "deploy_vps_auto.py"],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore',
    cwd="."
)

output = (result.stdout or "") + (result.stderr or "")

# Procurar por "Active: active" no output
if "Active: active" in output and "smindeck-bot" in output:
    print("[+] Bot está RODANDO no VPS")
    print("\n[*] Verificando últimas linhas de status:")
    
    # Extrair linhas relevantes
    lines = output.split('\n')
    for i, line in enumerate(lines):
        if 'smindeck-bot' in line or 'Active:' in line or 'PID' in line:
            print(line)
else:
    print("[-] Bot NAO está rodando ou não conseguiu conectar")
    print("\n[*] Output completo:")
    print(output[-2000:])  # Últimas 2000 caracteres

print("\n" + "="*60)
print("[!] Se o bot está rodando mas não responde no Discord:")
print("    1. Verifica se o token do bot está correto em .env")
print("    2. Verifica se o bot foi adicionado ao servidor")
print("    3. Verifica os logs em /opt/smindeck-bot/debug.log")
print("="*60)
