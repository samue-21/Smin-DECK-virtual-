; Instalador do SminDeck Bot (Discord + API)
; Gere os executáveis com PyInstaller e depois compile este .iss no Inno Setup.

[Setup]
AppName=SminDeck Bot
AppVersion=1.0
DefaultDirName={localappdata}\SminDeckBot
DefaultGroupName=SminDeck Bot
OutputBaseFilename=SminDeckBot-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
LanguageDetectionMethod=locale
PrivilegesRequired=lowest

[Languages]
Name: "ptbr"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Files]
; Executáveis gerados pelo PyInstaller (coloque em dist\)
Source: "..\dist\discord_bot.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\api_server.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\start_bot.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\setup_token.exe"; DestDir: "{app}"; Flags: ignoreversion

; Arquivos de suporte
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\SETUP_DISCORD.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\requirements.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Iniciar Bot (Discord + API)"; Filename: "{app}\start_bot.exe"
Name: "{group}\Configurar Token"; Filename: "{app}\setup_token.exe"
Name: "{group}\Abrir Pasta do Bot"; Filename: "{app}"

[Run]
; Primeiro: Configurar token (obrigatório na primeira vez)
Filename: "{app}\setup_token.exe"; Description: "Configurar Token Discord"; Flags: nowait; StatusMsg: "Configurando token do Discord..."

; Segundo: Iniciar o Bot
Filename: "{app}\start_bot.exe"; Description: "Iniciar o Bot agora"; StatusMsg: "Ativando seu bot Discord, aguarde..."; Flags: nowait postinstall skipifsilent

[Tasks]
Name: "startup"; Description: "Iniciar o Bot com o Windows (usuário atual)"; GroupDescription: "Opções adicionais:"; Flags: unchecked

[Registry]
; Inicia com o Windows (usuário atual) se marcar a task
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "SminDeckBot"; ValueData: """{app}\start_bot.exe"""; Tasks: startup

[Code]
procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpFinished then
  begin
    MsgBox('✓ Bot Discord instalado com sucesso!'#13#13'O token foi configurado. O bot foi iniciado em background.'#13#13'Você pode fechar esta janela.',
      mbInformation, MB_OK);
  end;
end;
