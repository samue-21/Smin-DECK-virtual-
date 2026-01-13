@echo off
REM Script para conectar no VPS e executar comandos
REM Salva senha em variável local (temporária)

setlocal enabledelayedexpansion

set VPS_HOST=72.60.244.240
set VPS_USER=root
set VPS_PASSWORD=Amor180725###
set VPS_PATH=c:\Users\SAMUEL\Desktop\Smin-DECK virtual

REM Opções: enviar, logs, cmd
set ACAO=%1

if "%ACAO%"=="" (
    echo.
    echo ======================================
    echo  Automacao VPS - SminDeck Bot
    echo ======================================
    echo.
    echo Opcoes:
    echo   auto_vps.bat enviar    - Enviar bot.py e reiniciar
    echo   auto_vps.bat logs      - Ver logs do bot
    echo   auto_vps.bat status    - Ver status do bot
    echo.
    exit /b
)

if "%ACAO%"=="enviar" (
    echo.
    echo 1. Copiando bot.py...
    scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=nul "!VPS_PATH!\bot.py" !VPS_USER!@!VPS_HOST!:/opt/smindeck-bot/ 2>nul
    if !errorlevel! equ 0 (
        echo 2. Reiniciando bot...
        ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=nul !VPS_USER!@!VPS_HOST! "pkill -f 'python.*bot.py' 2>/dev/null; sleep 2; cd /opt/smindeck-bot && nohup python3 bot.py > bot_output.log 2>&1 &" 2>nul
        echo.
        echo 3. Esperando bot iniciar...
        timeout /t 2 /nobreak >nul
        echo.
        echo Ultimas linhas do log:
        ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=nul !VPS_USER!@!VPS_HOST! "tail -n 15 /opt/smindeck-bot/bot_output.log" 2>nul
    ) else (
        echo Erro ao copiar arquivo
    )
)

if "%ACAO%"=="logs" (
    echo.
    echo Ultimos 50 linhas do log:
    ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=nul !VPS_USER!@!VPS_HOST! "tail -n 50 /opt/smindeck-bot/bot_output.log" 2>nul
)

if "%ACAO%"=="status" (
    echo.
    ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=nul !VPS_USER!@!VPS_HOST! "ps aux | grep python | grep -v grep" 2>nul
)

endlocal
