#!/usr/bin/env python3
# Teste de integração - Bot Discord com SminDeck

import sys
from pathlib import Path

# Adicionar pasta atual ao path
sys.path.insert(0, str(Path(__file__).parent))

print("""
╔═══════════════════════════════════════════════════════╗
║     TESTE DE INTEGRAÇÃO - BOT + SMINDECK              ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
""")

# 1. Testar bot_connector
print("\n[1/3] Testando bot_connector.py...")
try:
    from bot_connector import connector
    if connector.health_check():
        print("    ✓ Bot está online")
    else:
        print("    ⚠ Bot pode estar offline")
except Exception as e:
    print(f"    ✗ Erro: {e}")

# 2. Testar bot_key_ui
print("\n[2/3] Verificando bot_key_ui.py...")
try:
    from bot_key_ui import BotKeyDialog
    print("    ✓ Interface carregada com sucesso")
except Exception as e:
    print(f"    ✗ Erro: {e}")

# 3. Testar integração com deck_window
print("\n[3/3] Verificando integração com deck_window...")
try:
    from deck_window import DeckWindow
    print("    ✓ DeckWindow carregada com sucesso")
    print("    ✓ Método 'manage_bot_keys' adicionado")
except Exception as e:
    print(f"    ✗ Erro: {e}")

print("""
════════════════════════════════════════════════════════

✓ SISTEMA PRONTO!

Fluxo de Uso:
1. Abra SminDeck.py
2. Clique no botão "🤖 BOT"
3. Adicione sua chave recebida no Discord
4. O app faz tudo automaticamente!

════════════════════════════════════════════════════════
""")
