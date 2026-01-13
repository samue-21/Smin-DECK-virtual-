@echo off
REM Script para verificar logs do bot no VPS

echo.
echo [VERIFICANDO STATUS DO BOT]
echo ================================================
echo|set /p="Digite a senha do VPS (Amor180725###): "
setlocal enabledelayedexpansion

REM Usar plink para SSH com senha (mesmo de putty)
REM plink -pw senha usuario@host "comando"

echo.
echo Conectando ao VPS...
echo.

REM 1. Status do bot
echo.
echo ================================================
echo [STATUS DO BOT]
echo ================================================
plink -pw Amor180725### -l root 72.60.244.240 "systemctl status smindeck-bot"

REM 2. Ver logs
echo.
echo ================================================
echo [ULTIMAS 50 LINHAS DOS LOGS]
echo ================================================
plink -pw Amor180725### -l root 72.60.244.240 "tail -50 /opt/smindeck-bot/debug.log"

REM 3. Procurar erros
echo.
echo ================================================
echo [ERROS RECENTES]
echo ================================================
plink -pw Amor180725### -l root 72.60.244.240 "grep -i error /opt/smindeck-bot/debug.log | tail -20"

echo.
echo Verificacao concluida!
pause
