@echo off
REM ============================================================================
REM  TESTE COMPLETO - ARQUIVO SISTEMA AUTOMATIZADO
REM ============================================================================
REM
REM  Este script inicia automaticamente:
REM  1. Terminal com BOT
REM  2. Terminal com MONITOR
REM  3. Terminal com TESTE
REM
REM  Uso: teste_automatico.bat
REM ============================================================================

setlocal enabledelayedexpansion

cd /d "C:\Users\SAMUEL\Desktop\Smin-DECK virtual"

echo.
echo ============================================================================
echo  TESTE COMPLETO - SISTEMA DE ARQUIVOS END-TO-END
echo ============================================================================
echo.
echo [1] Iniciando BOT...
echo     Aguarde connexao ao Discord...
echo.

start "BOT - Smin-DECK" cmd /k "python bot.py"

timeout /t 5 /nobreak

echo.
echo [2] Iniciando MONITOR DE DEBUG...
echo     Atualizacoes a cada 3 segundos...
echo.

start "MONITOR - Debug" cmd /k "python monitor_debug.py"

timeout /t 3 /nobreak

echo.
echo [3] Iniciando TESTE COMPLETO...
echo     Aguardando arquivo via Discord...
echo.

start "TESTE - End-to-End" cmd /k "python teste_completo_end_to_end.py"

echo.
echo ============================================================================
echo JANELAS ABERTAS:
echo ============================================================================
echo [BOT]     - Conectando ao Discord, aguardando comandos
echo [MONITOR] - Monitorando banco, downloads e logs em tempo real
echo [TESTE]   - Aguardando você enviar arquivo via Discord
echo.
echo PROXIMOS PASSOS:
echo ============================================================================
echo 1. No Discord, digite: oi
echo 2. Escolha tipo: video ou imagem
echo 3. Escolha numero do botao (0-4)
echo 4. Envie um arquivo (attachment, URL ou ZIP)
echo 5. Digite nome personalizado
echo 6. Aguarde teste completar
echo.
echo O teste vai mostrar:
echo   - [PASSO 1] Arquivo sobe para banco
echo   - [PASSO 2] Dados no banco (chave, tamanho, nome, formato)
echo   - [PASSO 3] Sincronizador baixa arquivo
echo   - [PASSO 4] Arquivo em formato correto
echo.
echo ============================================================================
echo RESULTADO:
echo ============================================================================
echo [SUCCESS] = Fluxo funcionando! (Fazer git commit)
echo [FAIL]    = Algo deu errado (verificar logs em MONITOR)
echo.
pause
