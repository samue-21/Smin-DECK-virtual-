# Script de compilação - roda sem interrupções
$startTime = Get-Date

Write-Host "Iniciando compilação PyInstaller..." -ForegroundColor Cyan
Write-Host "Timestamp: $startTime" -ForegroundColor Gray

# Limpar builds anteriores
Write-Host "Removendo builds anteriores..." -ForegroundColor Yellow
Remove-Item -Path "build", "dist" -Recurse -Force -ErrorAction SilentlyContinue | Out-Null
Start-Sleep -Seconds 1

# Iniciar compilação
Write-Host "Compilando com PyInstaller..." -ForegroundColor Cyan
& python -m PyInstaller SminDeck.spec 2>&1 | ForEach-Object {
    if ($_ -match "INFO:|WARNING:|ERROR:") {
        Write-Host $_
    }
}

# Verificar resultado
$endTime = Get-Date
$duration = ($endTime - $startTime).TotalSeconds

if (Test-Path "dist\SminDeck.exe") {
    $file = Get-Item "dist\SminDeck.exe"
    $sizeMB = [math]::Round($file.Length / 1MB, 2)
    Write-Host "`nCOMPILACÃO CONCLUÍDA COM SUCESSO!" -ForegroundColor Green
    Write-Host "Arquivo: $($file.Name)" -ForegroundColor Green
    Write-Host "Tamanho: $sizeMB MB" -ForegroundColor Green
    Write-Host "Tempo total: $([math]::Round($duration, 1))s" -ForegroundColor Green
} else {
    Write-Host "`nERRO: Arquivo SminDeck.exe não foi criado!" -ForegroundColor Red
    Write-Host "Verifique os logs acima para detalhes." -ForegroundColor Red
}
