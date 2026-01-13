@echo off
cd /d C:\Users\SAMUEL\Desktop\SminDeck-Bot-Discord\installer
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" SminDeckBot.iss
if errorlevel 1 (
    echo Erro ao compilar
    pause
    exit /b 1
)
echo Recompilacao concluida
pause
