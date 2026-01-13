@echo off
REM Iniciar sistema SminDeck com banco de dados centralizado

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  SminDeck - Sistema com Banco Centralizado                ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

setlocal enabledelayedexpansion

if "%1"=="" (
    echo Uso: start_system.bat [comando]
    echo.
    echo Comandos disponíveis:
    echo   verify   - Verificação rápida do sistema
    echo   test-api - Testa todos os endpoints da API
    echo   test-flow - Testa fluxo completo
    echo   test-real - Instruções para teste real
    echo   app      - Inicia o APP SminDeck
    echo.
    goto :eof
)

if "%1"=="verify" (
    python verificar_sistema.py
    goto :eof
)

if "%1"=="test-api" (
    python test_api.py
    goto :eof
)

if "%1"=="test-flow" (
    python test_fluxo_completo.py
    goto :eof
)

if "%1"=="test-real" (
    python TESTE_REAL_INSTRUCOES.py
    goto :eof
)

if "%1"=="app" (
    python main.py
    goto :eof
)

echo Comando desconhecido: %1
