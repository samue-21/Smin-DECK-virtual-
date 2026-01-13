@echo off
setlocal

REM Script para compilar o instalador do SminDeck Bot com Inno Setup

cd /d C:\Users\SAMUEL\Desktop\SminDeck-Bot-Discord\installer

echo [BUILD] Compilando SminDeckBot-Setup.exe com Inno Setup...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" SminDeckBot.iss

if errorlevel 1 (
    echo [ERRO] Falha na compilacao do instalador
    exit /b 1
)

echo [SUCESSO] SminDeckBot-Setup.exe compilado em Output\SminDeckBot-Setup.exe
pause
