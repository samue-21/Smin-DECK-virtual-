#!/usr/bin/env python3
"""
✅ Verificação rápida de todos os componentes antes de teste real
"""

import subprocess
import sys
import time
from database_client import DatabaseClient

def check(name, condition):
    """Verifica condição e mostra status"""
    status = "✅" if condition else "❌"
    print(f"{status} {name}")
    return condition

def main():
    print("\n" + "="*60)
    print("🔍 VERIFICAÇÃO PRÉ-TESTE")
    print("="*60 + "\n")
    
    all_ok = True
    
    # 1. Verificar API
    print("1️⃣  VERIFICANDO API NA VPS...")
    client = DatabaseClient()
    api_ok = check("API online", client.health_check())
    all_ok = all_ok and api_ok
    print()
    
    # 2. Verificar database.py local
    print("2️⃣  VERIFICANDO DATABASE.PY LOCAL...")
    try:
        from database import init_database, criar_chave
        db_ok = check("Database.py importável", True)
        all_ok = all_ok and db_ok
    except Exception as e:
        db_ok = check(f"Database.py importável", False)
        print(f"   ⚠️  Erro: {e}")
        all_ok = False
    print()
    
    # 3. Verificar database_client.py
    print("3️⃣  VERIFICANDO DATABASE_CLIENT.PY...")
    try:
        dc_ok = check("DatabaseClient importável", True)
        all_ok = all_ok and dc_ok
    except Exception as e:
        dc_ok = check("DatabaseClient importável", False)
        print(f"   ⚠️  Erro: {e}")
        all_ok = False
    print()
    
    # 4. Verificar loading_dialog.py
    print("4️⃣  VERIFICANDO LOADING_DIALOG.PY...")
    try:
        from loading_dialog import LoadingDialog
        ld_ok = check("LoadingDialog importável", True)
        all_ok = all_ok and ld_ok
    except Exception as e:
        ld_ok = check("LoadingDialog importável", False)
        print(f"   ⚠️  Erro: {e}")
        all_ok = False
    print()
    
    # 5. Verificar bot_key_ui.py
    print("5️⃣  VERIFICANDO BOT_KEY_UI.PY...")
    try:
        from bot_key_ui import BotConnectionThread
        bku_ok = check("BotConnectionThread importável", True)
        all_ok = all_ok and bku_ok
    except Exception as e:
        bku_ok = check("BotConnectionThread importável", False)
        print(f"   ⚠️  Erro: {e}")
        all_ok = False
    print()
    
    # 6. Teste rápido de criar chave
    print("6️⃣  TESTE RÁPIDO - CRIAR CHAVE...")
    try:
        chave = client.criar_chave(111111111, 222222222, 333333333)
        chave_ok = check(f"Chave criada ({chave})", bool(chave))
        all_ok = all_ok and chave_ok
    except Exception as e:
        chave_ok = check("Chave criada", False)
        print(f"   ⚠️  Erro: {e}")
        all_ok = False
    print()
    
    # 7. Teste de validar chave
    print("7️⃣  TESTE RÁPIDO - VALIDAR CHAVE...")
    if chave:
        try:
            sucesso, msg = client.validar_chave(chave, 111111111, 222222222, 333333333)
            valida_ok = check(f"Chave validada ({msg})", sucesso)
            all_ok = all_ok and valida_ok
        except Exception as e:
            valida_ok = check("Chave validada", False)
            print(f"   ⚠️  Erro: {e}")
            all_ok = False
    print()
    
    # Resultado final
    print("="*60)
    if all_ok:
        print("🎉 TUDO OK! Pronto para teste real!")
        print("="*60)
        print("""
        Próximos passos:
        1. Execute: python TESTE_REAL_INSTRUCOES.py
        2. Siga as instruções detalhadas
        3. Teste com bot Discord real
        
        Comandos úteis:
        - python test_api.py (teste todos endpoints)
        - python test_fluxo_completo.py (simula fluxo)
        - python main.py (inicia APP com sync)
        """)
        return 0
    else:
        print("⚠️  ALGUNS ITENS FALHARAM")
        print("="*60)
        print("Verifique os erros acima e tente novamente")
        return 1

if __name__ == '__main__':
    sys.exit(main())
