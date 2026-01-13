#!/usr/bin/env python3
import paramiko
import json
from datetime import datetime

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("72.60.244.240", 22, "root", "Amor180725###", timeout=10)

# Criar conteúdo correto
version_data = {
    "version": "1.0.3",
    "download_url": "http://72.60.244.240:8000/download/smin_deck_v1.0.3_20260113_193224.zip",
    "changelog": "Versão 1.0.3 - Setup com auto-updater funcional",
    "released": datetime.now().isoformat(),
    "file_size": 39522
}

# Escrever via SSH
import tempfile
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump(version_data, f, indent=2)
    temp_file = f.name

# Upload do arquivo
sftp = ssh.open_sftp()
sftp.put(temp_file, "/root/smin_deck_updates/current_version.json")
sftp.close()

print("✅ Arquivo current_version.json atualizado")

import os
os.remove(temp_file)

ssh.close()
