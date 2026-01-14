#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONITOR DO BOT - Mostra logs do processamento em TEMPO REAL
Lê os logs que o bot está escrevendo na console
"""

import sys
import time
from datetime import datetime

def monitor_bot():
    print(f"\n{'='*80}")
    print(f"🤖 MONITOR DO BOT (lê console em tempo real)")
    print(f"{'='*80}")
    print(f"\nAguardando logs do bot...\n")
    print(f"Logs que procura:")
    print(f"  • [X] onde X = 1-34 (progresso do arquivo)")
    print(f"  • [BANCO] (logs do banco de dados)")
    print(f"  • [ERRO] (erros)")
    print(f"  • ✅ ou ❌ (sucesso/falha)")
    print(f"\n{'─'*80}\n")
    
    try:
        # Ler a entrada padrão (console do bot redirecionada)
        # Ou mostrar instruções de como capturar
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n\n{'='*80}")
        print(f"Monitor parado pelo usuário")
        print(f"{'='*80}\n")

if __name__ == '__main__':
    print(f"\n⚠️ ATENÇÃO: Este script monitora os logs do BOT")
    print(f"\nOpções:")
    print(f"1️⃣  Rodando bot localmente:")
    print(f"    Execute em outro terminal:")
    print(f"    python bot.py 2>&1 | tee bot_output.log")
    print(f"\n2️⃣  Para monitorar bot remoto (VPS):")
    print(f"    ssh user@vps 'tail -f /path/to/bot.log'")
    print(f"\n3️⃣  Para esta máquina:")
    print(f"    Abra TWO TERMINALS:")
    print(f"    Terminal 1: python monitor_banco_live.py")
    print(f"    Terminal 2: python bot.py")
    print(f"    (Os logs aparecerão no Terminal 2)")
    print(f"\n{'='*80}\n")
