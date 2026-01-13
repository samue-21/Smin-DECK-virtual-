#!/usr/bin/env python3
"""
Deploy dos arquivos para o VPS
Copia os arquivos modificados para o servidor
"""

import subprocess
import sys

arquivos = [
    "arquivo_processor.py",
    "bot.py",
    "api_server.py", 
    "sincronizador.py",
    "deck_window.py",
    "main.py"
]

vps_host = "root@72.60.244.240"
vps_path = "/opt/smindeck-bot/"
app_path = "/home/samuel/Desktop/Smin-DECK virtual/"

print("🚀 Iniciando deploy para VPS...")

for arquivo in arquivos:
    try:
        print(f"\n📤 Enviando {arquivo}...")
        cmd = f"scp {app_path}{arquivo} {vps_host}:{vps_path}"
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ {arquivo} enviado!")
    except Exception as e:
        print(f"❌ Erro ao enviar {arquivo}: {e}")
        sys.exit(1)

print("\n✅ Deploy concluído!")
print("\n📝 Próximos passos:")
print("1. ssh root@72.60.244.240")
print("2. systemctl restart smindeck-bot")
print("3. systemctl restart smindeck-api")
