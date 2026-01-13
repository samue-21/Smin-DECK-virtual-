#define MyAppName "Smin-DECK"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Smin Solutions"
#define MyAppExeName "Smin-DECK.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL=https://smin-deck.com
AppSupportURL=https://smin-deck.com/suporte
DefaultDirName={pf}\Smin-DECK
DefaultGroupName={#MyAppName}
AllowNoIcons=no
PrivilegesRequired=admin
OutputDir=.\Output
OutputBaseFilename=Smin-DECK-Setup-v1.0.0
SetupIconFile=logo-5.ico
UninstallDisplayIcon={app}\Smin-DECK.exe
Compression=lzma
SolidCompression=yes
WizardStyle=modern
LanguageDetectionMethod=locale
ArchitecturesInstallIn64BitMode=x64
ArchitecturesAllowed=x64
LicenseFile=LICENCA.txt

[Languages]
Name: "ptbr"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunch"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1
Name: "klitecodecs"; Description: "Instalar K-Lite Codecs Standard (melhor suporte a vídeo)"; GroupDescription: "Componentes Adicionais"; Flags: unchecked

[Files]
; Smin-DECK Application
Source: "dist\Smin-DECK\Smin-DECK.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\Smin-DECK\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs

; Assets
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

; Configuração padrão
Source: "deck_config.sdk"; DestDir: "{app}"; Flags: ignoreversion

; Documentação
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\logo-5.ico"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\assets\logo-5.ico"

[Run]
; K-Lite Codecs (se selecionado)
Filename: "{app}\extras\Ninite KLite Codecs Installer.exe"; Description: "Instalando K-Lite Codecs..."; Tasks: klitecodecs; Flags: waituntilterminated
; Executar Smin-DECK
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent

[Code]
procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpSelectTasks then
  begin
    MsgBox('Recomenda-se instalar KLite Codecs para suporte completo a vídeos.', mbInformation, MB_OK);
  end;
end;

procedure InitializeWizard();
begin
  WizardForm.TasksList.Height := WizardForm.TasksList.Height + 20;
end;
