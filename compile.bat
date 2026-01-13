@echo off
REM Compilacao SminDeck com PyInstaller
echo Limpando builds anteriores...
rmdir /S /Q build dist 2>nul
timeout /t 2

echo Compilando SminDeck.exe...
python -m PyInstaller SminDeck-optimized.spec

if exist dist\SminDeck.exe (
    echo.
    echo ============================================
    echo Compilacao CONCLUIDA COM SUCESSO!
    echo ============================================
    dir /s dist\SminDeck.exe
) else (
    echo.
    echo ============================================
    echo ERRO: Arquivo nao foi criado
    echo ============================================
    pause
)
