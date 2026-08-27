; ============================================================
; CyberTools Suite - Inno Setup Installer Script
; ============================================================
; 1. Install Inno Setup (free): https://jrsoftware.org/isdl.php
; 2. Run installer\build_exe.bat FIRST (this script packages that output)
; 3. Open this file in Inno Setup, click Compile (or Build > Compile)
; 4. Output/Setup.exe is your final installer - this is what you share
; ============================================================

#define MyAppName "CyberTools Suite"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "CyberTools"
#define MyAppExeName "CyberToolsSuite.exe"
#define MyAppCopyright "Copyright © 2026 CyberTools. All Rights Reserved."

[Setup]
AppId={{8F3A2C10-4B5E-4A7D-9C1E-CYBERTOOLS01}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppCopyright={#MyAppCopyright}
DefaultDirName={localappdata}\CyberTools Suite
DefaultGroupName=CyberTools Suite
DisableProgramGroupPage=yes
OutputDir=Output
OutputBaseFilename=CyberToolsSuite_Setup_v{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=..\assets\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
ArchitecturesInstallIn64BitMode=x64
LicenseFile=..\LICENSE.txt
InfoBeforeFile=..\README.txt
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\altaf\OneDrive\Desktop\CyberToolsSuite\CyberToolsSuite\dist\CyberToolsSuite\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Start Menu shortcut (created automatically on install)
Name: "{group}\CyberTools Suite"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall CyberTools Suite"; Filename: "{uninstallexe}"
; Desktop shortcut (created automatically on install)
Name: "{autodesktop}\CyberTools Suite"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,CyberTools Suite}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Leave user's cases/reports alone on uninstall - only clean install files
Type: filesandordirs; Name: "{app}\build"
Type: filesandordirs; Name: "{app}\cases"
Type: filesandordirs; Name: "{app}\reports"