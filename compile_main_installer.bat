@echo off
setlocal

REM Script para compilar o instalador principal do SminDeck

cd /d "c:\Users\SAMUEL\Desktop\Smin-DECK virtual"

echo [BUILD] Compilando SminDeck-Setup.exe com Inno Setup...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss

if errorlevel 1 (
    echo [ERRO] Falha na compilacao do instalador principal
    exit /b 1
)

echo.
echo [SUCESSO] SminDeck-Setup.exe compilado com sucesso em dist\SminDeck-Setup.exe
echo.
