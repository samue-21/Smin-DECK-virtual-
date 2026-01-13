#!/usr/bin/env python3
"""
Script para compilar o SminDeck com PyInstaller
"""
import os
import subprocess
import sys

def build():
    # Caminho base
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, "assets", "logo-5.ico")
    
    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "SminDeck",
        "--icon", icon_path,
        "--add-data", f"{icon_path};.",
        "--distpath", os.path.join(base_dir, "dist"),
        "--workpath", os.path.join(base_dir, "build"),
        "--specpath", os.path.join(base_dir, "build"),
        "--collect-all", "PyQt6",
        "main.py"
    ]
    
    print("🔨 Compilando SminDeck...")
    print(f"Comando: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, cwd=base_dir)
        if result.returncode == 0:
            print("\n✅ Compilação concluída com sucesso!")
            print(f"📦 Executável em: {os.path.join(base_dir, 'dist', 'SminDeck.exe')}")
        else:
            print("\n❌ Erro na compilação!")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build()
