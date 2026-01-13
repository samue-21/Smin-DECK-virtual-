#!/usr/bin/env powershell
# Instalador SminDeck
# Este script instala o SminDeck em Program Files

param(
    [string]$InstallPath = "C:\Program Files\SminDeck"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Instalador SminDeck v1.2" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

# Verificar direitos de admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "Erro: Este instalador requer direitos de administrador!" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Criar pasta de instalacao
Write-Host "Criando pasta: $InstallPath" -ForegroundColor Yellow
if (Test-Path $InstallPath) {
    Remove-Item $InstallPath -Recurse -Force -ErrorAction SilentlyContinue
}
New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null

# Copiar arquivo executavel
Write-Host "Copiando SminDeck.exe..." -ForegroundColor Yellow
if (Test-Path "dist\SminDeck.exe") {
    Copy-Item "dist\SminDeck.exe" "$InstallPath\SminDeck.exe" -Force
    Write-Host "OK!" -ForegroundColor Green
} else {
    Write-Host "Erro: SminDeck.exe nao encontrado!" -ForegroundColor Red
    exit 1
}

# Copiar assets se existirem
if (Test-Path "assets") {
    Write-Host "Copiando assets..." -ForegroundColor Yellow
    Copy-Item "assets" "$InstallPath\assets" -Recurse -Force
    Write-Host "OK!" -ForegroundColor Green
}

# Criar atalho no Menu Iniciar
Write-Host "Criando atalho no Menu Iniciar..." -ForegroundColor Yellow
$startMenuPath = "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\SminDeck"
New-Item -ItemType Directory -Path $startMenuPath -Force -ErrorAction SilentlyContinue | Out-Null

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut("$startMenuPath\SminDeck.lnk")
$shortcut.TargetPath = "$InstallPath\SminDeck.exe"
$shortcut.WorkingDirectory = $InstallPath
$shortcut.IconLocation = "$InstallPath\assets\logo-5.ico"
$shortcut.Save()
Write-Host "OK!" -ForegroundColor Green

# Criar atalho na area de trabalho
Write-Host "Criando atalho na Area de Trabalho..." -ForegroundColor Yellow
$desktopPath = [Environment]::GetFolderPath("Desktop")
$desktopShortcut = $shell.CreateShortcut("$desktopPath\SminDeck.lnk")
$desktopShortcut.TargetPath = "$InstallPath\SminDeck.exe"
$desktopShortcut.WorkingDirectory = $InstallPath
$desktopShortcut.IconLocation = "$InstallPath\assets\logo-5.ico"
$desktopShortcut.Save()
Write-Host "OK!" -ForegroundColor Green

# Sucesso
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "INSTALACAO CONCLUIDA COM SUCESSO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Pasta de instalacao: $InstallPath" -ForegroundColor Cyan
Write-Host "Voce pode iniciar o SminDeck do:" -ForegroundColor Cyan
Write-Host "  1. Menu Iniciar -> SminDeck" -ForegroundColor White
Write-Host "  2. Area de Trabalho" -ForegroundColor White
Write-Host ""
$launchChoice = Read-Host "Deseja iniciar o SminDeck agora? (S/N)"
if ($launchChoice -eq 'S' -or $launchChoice -eq 's') {
    & "$InstallPath\SminDeck.exe"
}
