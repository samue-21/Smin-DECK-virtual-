#!/usr/bin/env pwsh
# Script para conectar ao VPS com senha usando sshpass

$VPS_IP = "72.60.244.240"
$VPS_PASSWORD = "Amor180725###"
$VPS_USER = "root"

# Instalar sshpass se não existir
if (-not (Get-Command sshpass -ErrorAction SilentlyContinue)) {
    Write-Host "Instalando sshpass..." -ForegroundColor Yellow
    choco install sshpass -y
}

# Executar comando com sshpass
Write-Host "Conectando ao VPS..." -ForegroundColor Cyan
$env:SSHPASS = $VPS_PASSWORD

sshpass -e ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=$null "$VPS_USER@$VPS_IP" "
echo '=== Status do Bot ==='
systemctl status smindeck-bot --no-pager

echo ''
echo '=== Últimas 50 linhas do Log ==='
tail -50 /opt/smindeck-bot/debug.log

echo ''
echo '=== Processos Python ==='
ps aux | grep python3 | grep -v grep
"

$env:SSHPASS = ""
