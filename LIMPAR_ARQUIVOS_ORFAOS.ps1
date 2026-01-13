# Script de Limpeza de Arquivos Orfaos - SminDeck
# Este script move arquivos nao utilizados para uma pasta de backup

$projectDir = "C:\Users\SAMUEL\Desktop\Smin-DECK virtual"
$backupDir = Join-Path $projectDir "_BACKUP_ARQUIVOS_ORFAOS_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

# Lista de arquivos orfaos a remover
$orphaned = @(
    "ATIVAR_MESSAGE_CONTENT.py",
    "RESUMO_FINAL.py",
    "TESTE_CLIENTE_GUIA.py",
    "TESTE_REAL_INSTRUCOES.py",
    "analisar_bot_code.py",
    "auto_vps.py",
    "bot_client.py",
    "bot_client_remote.py",
    "bot_file_sync.py",
    "bot_humanizado_interativo.py",
    "build_exe.py",
    "check_api.py",
    "check_api_status.py",
    "check_bot.py",
    "check_bot_logs.py",
    "check_databases.py",
    "check_db.py",
    "check_db_local.py",
    "check_logs.py",
    "check_logs_vps.py",
    "check_updates.py",
    "check_vps_db.py",
    "check_vps_env.py",
    "check_vps_files.py",
    "check_vps_logs.py",
    "check_vps_status.py",
    "cleanup.py",
    "corrigir_vps.py",
    "criar_api.py",
    "criar_api_service.py",
    "db_temp.py",
    "debug_bin_files.py",
    "debug_loading.py",
    "debug_obter_info.py",
    "debug_pos_validacao.py",
    "debug_usuario_auth.py",
    "debug_validacao.py",
    "demo_client_usage.py",
    "deploy_app.py",
    "deploy_automatico.py",
    "deploy_bot.py",
    "deploy_bot_fix.py",
    "deploy_bot_vps.py",
    "deploy_vps.py",
    "deploy_vps_auto.py",
    "discord_auth_ui.py",
    "discord_bot.py",
    "discord_oauth.py",
    "enviar_bot_corrigido.py",
    "executar_smindeck.py",
    "fix_api_port.py",
    "fix_api_server.py",
    "fix_port_5001.py",
    "fix_vps_dependencies.py",
    "fix_vps_index.py",
    "launcher.py",
    "ler_completo_bot.py",
    "ler_funcoes_bot.py",
    "limpar_atualizacoes_remoto.py",
    "limpar_atualizacoes_remoto_v2.py",
    "limpar_atualizacoes_remoto_v3.py",
    "make_icon.py",
    "monitorar_bot.py",
    "notify_bot.py",
    "quick_fix_playwright.py",
    "restart_bot.py",
    "run_smindeck.py",
    "setup_api.py",
    "setup_cliente_completo.py",
    "setup_token.py",
    "start_api.py",
    "start_bot_launcher.py",
    "test_api.py",
    "test_auto_renomear.py",
    "test_bot_status.py",
    "test_discord_connection.py",
    "test_download_manager.py",
    "test_fluxo_completo.py",
    "test_full_flow.py",
    "test_integration.py",
    "test_sync_final.py",
    "test_url_direct.py",
    "test_window.py",
    "test_youtube.py",
    "teste_loading_condicional.py",
    "verificar_sistema.py",
    "vps_logs.py"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "LIMPEZA DE ARQUIVOS ORFAOS - SMIN-DECK" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Criar pasta de backup
Write-Host "Criando pasta de backup..." -ForegroundColor Yellow
if (!(Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir | Out-Null
    Write-Host "Pasta criada: $backupDir" -ForegroundColor Green
} else {
    Write-Host "Pasta ja existe: $backupDir" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Movendo arquivos orfaos..." -ForegroundColor Yellow
Write-Host ""

$movedCount = 0
$notFoundCount = 0

foreach ($file in $orphaned) {
    $filePath = Join-Path $projectDir $file
    
    if (Test-Path $filePath) {
        try {
            Move-Item -Path $filePath -Destination $backupDir -Force
            Write-Host "[OK] Movido: $file" -ForegroundColor Green
            $movedCount++
        } catch {
            Write-Host "[ERRO] Nao foi possivel mover: $file - $_" -ForegroundColor Red
        }
    } else {
        Write-Host "[NAO ENCONTRADO] $file" -ForegroundColor Gray
        $notFoundCount++
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "RESUMO DA LIMPEZA" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Arquivos movidos: $movedCount" -ForegroundColor Green
Write-Host "Arquivos nao encontrados: $notFoundCount" -ForegroundColor Yellow
Write-Host "Total processado: $($orphaned.Count)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pasta de backup: $backupDir" -ForegroundColor Green
Write-Host ""
Write-Host "Operacao concluida com sucesso!" -ForegroundColor Green
