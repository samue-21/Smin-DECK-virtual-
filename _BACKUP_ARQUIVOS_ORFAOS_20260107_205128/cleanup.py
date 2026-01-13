#!/usr/bin/env python3
"""
Limpa arquivos antigos de deploy/debug que não são mais necessários
Mantém apenas auto_vps.py para comunicação com VPS
"""

import os
from pathlib import Path

# Arquivos antigos que podem ser deletados
ARQUIVOS_OBSOLETOS = [
    'reset_chave_dialog.py',
    'deploy_auto.py',
    'gerenciar_bot.py',
    'atualizar_token.py',
    'deploy_complete.py',
    'limpar_chaves_antigas.py',
    'verificar_bot_vps.py',
    'verificar_bot_vps_v2.py',
    'testar_criar_chave.py',
    'ver_database.py',
    'limpeza_completa_vps.py',
    'debug_bot_criacao.py',
    'corrigir_bug_autenticacao.py',
    'reiniciar_bot.py',
    'adicionar_logs_bot.py',
    'verificar_bot_atual.py',
    'verificar_correcao.py',
    'verificar_logs_bot.py',
    'verif_atualizacoes.py',
    'ver_debug_log.py',
    'ver_log_bot.py',
    'ver_log_completo.py',
    'verificar_bot.py',
    'testar_reset.py',
    'sync_bot_vps.py',
    'restaurar_bot.py',
    'monitor_bot.py',
    'enviar_bot_sftp.py',
    'enviar_bot_debug.py',
]

def limpar():
    base_path = Path(os.getcwd())
    deletados = []
    
    for arquivo in ARQUIVOS_OBSOLETOS:
        full_path = base_path / arquivo
        if full_path.exists():
            try:
                full_path.unlink()
                deletados.append(arquivo)
                print(f"✅ Deletado: {arquivo}")
            except Exception as e:
                print(f"❌ Erro ao deletar {arquivo}: {e}")
        else:
            print(f"⏭️  Pulado (não encontrado): {arquivo}")
    
    print(f"\n✅ Limpeza completa! {len(deletados)} arquivos deletados.")
    print("\n📋 Arquivos que você ainda tem:")
    print("  - auto_vps.py     (principal para comunicação com VPS)")
    print("  - vps_config.py   (configuração de acesso)")
    print("  - monitorar_bot.py (monitorar logs em tempo real)")

if __name__ == "__main__":
    resposta = input("Deseja deletar todos os scripts antigos? (s/n): ").lower()
    if resposta == 's':
        limpar()
    else:
        print("Operação cancelada")
