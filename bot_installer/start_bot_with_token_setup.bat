@echo off
REM Script simples para iniciar o bot com configuração de token se necessário

setlocal enabledelayedexpansion

cd /d "%~dp0"

REM Verifica se .env existe
if not exist ".env" (
    echo Configurando token do Discord na primeira execucao...
    echo.
    call setup_token.exe
    if errorlevel 1 (
        echo Falha na configuracao do token. Abortando.
        pause
        exit /b 1
    )
)

REM Verifica se token está vazio
for /f "delims==" %%A in ('type .env ^| find "DISCORD_TOKEN=" 2^>nul') do (
    set "TOKEN_VALUE=%%A"
)

if "!TOKEN_VALUE!"=="" (
    echo Token nao configurado. Executando setup_token.exe...
    call setup_token.exe
)

REM Inicia os serviços silenciosamente
echo Iniciando servicos do bot...
start /b discord_bot.exe
start /b api_server.exe

echo Bot iniciado em background. Voce pode fechar esta janela.
exit /b 0
