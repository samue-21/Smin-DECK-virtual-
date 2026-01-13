@echo off
REM Build Script para SminDeck
REM Compila o arquivo main.py para um executável standalone

setlocal enabledelayedexpansion

echo.
echo ==================================================
echo  🔨 SminDeck Build Script
echo ==================================================
echo.

REM Verificar se o Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Instale Python 3.9+
    pause
    exit /b 1
)

REM Verificar se PyInstaller está instalado
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando PyInstaller...
    pip install pyinstaller
)

REM Limpar builds anteriores
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

echo.
echo 🔨 Compilando SminDeck...
echo.

REM Comando de compilação
pyinstaller --onefile ^
    --windowed ^
    --name "SminDeck" ^
    --icon="assets\logo-5.ico" ^
    --add-data "assets\logo-5.ico;." ^
    --collect-all PyQt6 ^
    main.py

if errorlevel 1 (
    echo.
    echo ❌ Erro na compilação!
    pause
    exit /b 1
)

echo.
echo ✅ Compilação concluída com sucesso!
echo.
echo 📦 Executável gerado em: dist\SminDeck.exe
echo.

REM Se o instalador do bot existir no projeto, copie para dist\ para facilitar o bundling no setup principal
if exist "bot_installer\SminDeckBot-Setup.exe" (
    echo 📦 Copiando instalador do bot para dist\...
    copy /y "bot_installer\SminDeckBot-Setup.exe" "dist\SminDeckBot-Setup.exe" >nul
    if errorlevel 1 (
        echo ⚠️  Não foi possível copiar o instalador do bot para dist\
    ) else (
        echo ✅ Bot installer copiado: dist\SminDeckBot-Setup.exe
    )
) else (
    echo ℹ️  Instalador do bot não encontrado em bot_installer\SminDeckBot-Setup.exe
)

pause
