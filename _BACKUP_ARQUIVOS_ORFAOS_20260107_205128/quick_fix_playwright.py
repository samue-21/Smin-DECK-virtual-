#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instalar dependências do Playwright de forma rápida e não-interativa
"""

import paramiko
import sys
import os

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

VPS_HOST = "72.60.244.240"
VPS_USER = "root"
VPS_PASSWORD = "Amor180725###"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(VPS_HOST, username=VPS_USER, password=VPS_PASSWORD, timeout=10)

print("✅ Conectado\n")

# 1. Atualizar
print("1️⃣  Atualizando apt...")
ssh.exec_command("DEBIAN_FRONTEND=noninteractive apt-get update -qq 2>&1 &")

# 2. Instalar dependências críticas do Playwright
print("2️⃣  Instalando dependências de biblioteca...")
cmd = """DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
libatk-1.0-0 libatk-bridge2.0-0 libatspi2.0-0 libcairo2 libcups2 \
libdbus-1-3 libexpat1 libgbm1 libgdk-pixbuf2.0-0 libglib2.0-0 \
libgtk-3-0 libgtk-3-common libice6 libpango-1.0-0 libpangocairo-1.0-0 \
libsm6 libwayland-client0 libwayland-cursor0 libwayland-egl1 libx11-6 \
libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 \
libxi6 libxinerama1 libxrandr2 libxrender1 libxss1 libxtst6 2>&1"""

stdin, stdout, stderr = ssh.exec_command(cmd)
stdout.channel.set_combine_stderr(True)
for line in stdout:
    pass  # Apenas consumir output

# 3. Reinstalar Chromium
print("3️⃣  Instalando Chromium do Playwright...")
ssh.exec_command("python3 -m playwright install chromium 2>&1 &")

# 4. Reiniciar bot
print("4️⃣  Reiniciando bot...")
ssh.exec_command("systemctl restart smindeck-bot")

print("\n✅ Comandos enviados! Bot deve estar ativo em alguns segundos...")

ssh.close()
