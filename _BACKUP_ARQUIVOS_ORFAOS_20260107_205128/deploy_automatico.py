#!/usr/bin/env python3
"""
Deploy automático para VPS com senha
Copia os arquivos e executa comandos no VPS
"""

import subprocess
import sys
import os

# ⚠️ CREDENCIAIS (guardar com segurança em produção)
VPS_HOST = "72.60.244.240"
VPS_USER = "root"
VPS_PASSWORD = "Amor180725###"
VPS_PATH = "/opt/smindeck-bot/"

ARQUIVOS = [
    "arquivo_processor.py",
    "bot.py",
    "api_server.py",
    "sincronizador.py",
    "deck_window.py",
]

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))

def run_command(cmd, description=""):
    """Executa comando e mostra saída"""
    if description:
        print(f"\n{description}")
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def deploy():
    """Deploy completo para o VPS"""
    
    print("=" * 60)
    print("🚀 DEPLOY AUTOMÁTICO - SminDeck")
    print("=" * 60)
    
    # Verificar se sshpass está instalado
    try:
        subprocess.run(["sshpass", "-V"], capture_output=True, check=True)
    except:
        print("❌ sshpass não está instalado!")
        print("\nInstale com:")
        print("  Windows (WSL): sudo apt install sshpass")
        print("  macOS: brew install sshpass")
        print("  Linux: sudo apt install sshpass")
        sys.exit(1)
    
    # 1️⃣ ENVIAR ARQUIVOS
    print("\n" + "=" * 60)
    print("📤 ENVIANDO ARQUIVOS PARA VPS")
    print("=" * 60)
    
    for arquivo in ARQUIVOS:
        local = os.path.join(LOCAL_PATH, arquivo)
        remote = f"root@{VPS_HOST}:{VPS_PATH}"
        
        cmd = f'sshpass -p "{VPS_PASSWORD}" scp {local} {remote}'
        print(f"\n📄 Enviando {arquivo}...")
        
        if run_command(cmd):
            print(f"✅ {arquivo} enviado!")
        else:
            print(f"❌ Erro ao enviar {arquivo}")
            sys.exit(1)
    
    # 2️⃣ CRIAR PASTA UPLOADS
    print("\n" + "=" * 60)
    print("📁 CRIANDO ESTRUTURA DE PASTAS")
    print("=" * 60)
    
    cmd = f'sshpass -p "{VPS_PASSWORD}" ssh {VPS_USER}@{VPS_HOST} mkdir -p /opt/smindeck-bot/uploads'
    if run_command(cmd, "Criando pasta uploads..."):
        print("✅ Pasta uploads criada!")
    
    # 3️⃣ INSTALAR DEPENDÊNCIAS
    print("\n" + "=" * 60)
    print("📦 INSTALANDO DEPENDÊNCIAS")
    print("=" * 60)
    
    commands = [
        ("apt update", "Atualizando pacotes..."),
        ("apt install -y ffmpeg", "Instalando ffmpeg..."),
        ("pip install Pillow aiohttp", "Instalando Python packages..."),
    ]
    
    for cmd, desc in commands:
        full_cmd = f'sshpass -p "{VPS_PASSWORD}" ssh {VPS_USER}@{VPS_HOST} "{cmd}"'
        if run_command(full_cmd, desc):
            print(f"✅ {desc.replace('...', '')} instalado!")
    
    # 4️⃣ VERIFICAR PERMISSÕES
    print("\n" + "=" * 60)
    print("🔐 AJUSTANDO PERMISSÕES")
    print("=" * 60)
    
    cmd = f'sshpass -p "{VPS_PASSWORD}" ssh {VPS_USER}@{VPS_HOST} "chmod 755 /opt/smindeck-bot/*.py && chmod 755 /opt/smindeck-bot/uploads"'
    if run_command(cmd, "Ajustando permissões..."):
        print("✅ Permissões ajustadas!")
    
    # 5️⃣ REINICIAR SERVIÇOS
    print("\n" + "=" * 60)
    print("🔄 REINICIANDO SERVIÇOS")
    print("=" * 60)
    
    services = [
        ("systemctl restart smindeck-bot", "Reiniciando bot..."),
        ("systemctl restart smindeck-api", "Reiniciando API..."),
    ]
    
    for cmd, desc in services:
        full_cmd = f'sshpass -p "{VPS_PASSWORD}" ssh {VPS_USER}@{VPS_HOST} "{cmd}"'
        if run_command(full_cmd, desc):
            print(f"✅ {desc.replace('...', '')} reiniciado!")
    
    # 6️⃣ VERIFICAR STATUS
    print("\n" + "=" * 60)
    print("✅ VERIFICANDO STATUS DOS SERVIÇOS")
    print("=" * 60)
    
    cmd = f'sshpass -p "{VPS_PASSWORD}" ssh {VPS_USER}@{VPS_HOST} "systemctl status smindeck-bot smindeck-api --no-pager"'
    run_command(cmd)
    
    # SUCESSO!
    print("\n" + "=" * 60)
    print("🎉 DEPLOY CONCLUÍDO COM SUCESSO!")
    print("=" * 60)
    print("\n📝 Próximos passos:")
    print("1. Abre o APP local")
    print("2. No Discord: envia 'oi'")
    print("3. Seleciona um botão")
    print("4. Seleciona 'Atualizar Vídeo' ou 'Atualizar Imagem'")
    print("5. Envia um arquivo (MP4, JPG, etc)")
    print("\n✅ O arquivo será processado e sincronizado automaticamente!")
    
    # Ver logs
    print("\n📊 Para ver logs em tempo real:")
    print(f'  sshpass -p "{VPS_PASSWORD}" ssh {VPS_USER}@{VPS_HOST} "tail -f /opt/smindeck-bot/debug.log"')

if __name__ == "__main__":
    try:
        deploy()
    except KeyboardInterrupt:
        print("\n\n❌ Deploy cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)
