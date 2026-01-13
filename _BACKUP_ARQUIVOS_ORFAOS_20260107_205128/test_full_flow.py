#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 TESTE COMPLETO DO SISTEMA
Valida todo o fluxo: Bot → API → Cliente
"""

import requests
import time
import json
from pathlib import Path

# Cores para terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

VPS_API = "http://72.60.244.240:5000"
TIMEOUT = 10

def print_test(name, status, detail=""):
    icon = f"{GREEN}✓{RESET}" if status else f"{RED}✗{RESET}"
    print(f"{icon} {name:<40} {YELLOW}{detail}{RESET}")

def separator():
    print(f"\n{BLUE}{'='*70}{RESET}\n")

def test_api_health():
    """Testa se a API está online"""
    print(f"\n{BLUE}[1/5] Testando Saúde da API{RESET}")
    try:
        response = requests.get(f"{VPS_API}/api/health", timeout=TIMEOUT)
        data = response.json()
        status = data.get("status") == "online"
        print_test("API Health Check", status, f"Status: {data.get('status')}")
        return status
    except Exception as e:
        print_test("API Health Check", False, str(e))
        return False

def test_connector_import():
    """Testa se o bot_connector pode ser importado"""
    print(f"\n{BLUE}[2/5] Testando Importação de bot_connector{RESET}")
    try:
        from bot_connector import connector
        print_test("Import bot_connector", True)
        print_test("Connector inicializado", True, f"Base URL: {connector.api_url}")
        return True
    except Exception as e:
        print_test("Import bot_connector", False, str(e))
        return False

def test_health_check_from_connector():
    """Testa health check via connector"""
    print(f"\n{BLUE}[3/5] Testando Health Check via Connector{RESET}")
    try:
        from bot_connector import connector
        is_online = connector.health_check()
        print_test("Connector.health_check()", is_online, f"Bot {'online' if is_online else 'offline'}")
        return is_online
    except Exception as e:
        print_test("Connector.health_check()", False, str(e))
        return False

def test_key_operations():
    """Testa operações de chave (sem adicionar permanentemente)"""
    print(f"\n{BLUE}[4/5] Testando Operações de Chave{RESET}")
    try:
        from bot_connector import connector
        
        # Listar chaves existentes
        keys = connector.list_keys()
        print_test("Listar chaves", True, f"Total: {len(keys)} chave(s)")
        
        if keys:
            print_test("Chaves encontradas", True, f"{keys}")
        else:
            print_test("Nenhuma chave armazenada", True, "Aguardando primeiro acesso")
        
        return True
    except Exception as e:
        print_test("Operações de chave", False, str(e))
        return False

def test_ui_imports():
    """Testa se as UIs podem ser importadas"""
    print(f"\n{BLUE}[5/5] Testando Importações de UI{RESET}")
    try:
        from bot_key_ui import BotKeyDialog, BotKeysListDialog, BotConnectionThread
        print_test("Import BotKeyDialog", True)
        print_test("Import BotKeysListDialog", True)
        print_test("Import BotConnectionThread", True)
        return True
    except Exception as e:
        print_test("Importação de UIs", False, str(e))
        return False

def main():
    print(f"\n{BLUE}╔════════════════════════════════════════════════════╗{RESET}")
    print(f"{BLUE}║{RESET}    🧪 TESTE COMPLETO DO SISTEMA SMINBOT{RESET}")
    print(f"{BLUE}║{RESET}    Validando: Bot → API → Cliente{RESET}")
    print(f"{BLUE}╚════════════════════════════════════════════════════╝{RESET}")
    
    separator()
    
    results = []
    
    # Executar testes
    results.append(("API Health", test_api_health()))
    results.append(("Bot Connector Import", test_connector_import()))
    results.append(("Health Check via Connector", test_health_check_from_connector()))
    results.append(("Key Operations", test_key_operations()))
    results.append(("UI Imports", test_ui_imports()))
    
    separator()
    
    # Resumo final
    passed = sum(1 for _, status in results if status)
    total = len(results)
    
    print(f"\n{BLUE}📊 RESUMO FINAL:{RESET}\n")
    
    for test_name, status in results:
        icon = f"{GREEN}✓{RESET}" if status else f"{RED}✗{RESET}"
        print(f"  {icon} {test_name:<30} {'PASSOU' if status else 'FALHOU'}")
    
    print(f"\n{BLUE}{'='*70}{RESET}")
    
    if passed == total:
        print(f"{GREEN}✓ SISTEMA PRONTO! Todos os {total} testes passaram!{RESET}\n")
        print(f"{GREEN}🚀 O cliente pode começar a usar agora!{RESET}\n")
        return 0
    else:
        print(f"{RED}✗ {total - passed} teste(s) falharam. Verifique os erros acima.{RESET}\n")
        return 1

if __name__ == "__main__":
    exit(main())
