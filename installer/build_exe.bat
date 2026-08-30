@echo off
REM ============================================================
REM CyberTools Suite - Build Script
REM Run this from the project root folder (where main.py lives):
REM     installer\build_exe.bat
REM Produces: dist\CyberToolsSuite\CyberToolsSuite.exe
REM ============================================================

cd /d "%~dp0\.."

REM Set Python path - apne venv ke hisaab se adjust karo
set PYTHON="C:\Users\altaf\OneDrive\Desktop\CyberToolsSuite\venv\Scripts\python.exe"
set PIP="C:\Users\altaf\OneDrive\Desktop\CyberToolsSuite\venv\Scripts\pip.exe"
set PYINSTALLER="C:\Users\altaf\OneDrive\Desktop\CyberToolsSuite\venv\Scripts\pyinstaller.exe"

echo.
echo ============================================================
echo           CyberTools Suite - Build Script
echo           Copyright (c) 2026 CyberTools
echo           All Rights Reserved
echo ============================================================
echo.

REM Check Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8+.
    pause
    exit /b 1
)

REM Check PyInstaller
python -m PyInstaller --version >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [1/4] Installing PyInstaller...
    pip install pyinstaller
) else (
    echo [1/4] PyInstaller already installed.
)

echo.
echo [2/4] Installing dependencies...
%PIP% install -r requirements.txt

echo.
echo [3/4] Cleaning previous build...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul

echo.
echo [4/4] Building CyberToolsSuite.exe with PyInstaller...

%PYINSTALLER% main.py ^
    --name "CyberToolsSuite" ^
    --windowed ^
    --icon "assets\icon.ico" ^
    --add-data "engines;engines" ^
    --add-data "data;data" ^
    --add-data "assets;assets" ^
    --hidden-import "PySide6.QtSvg" ^
    --hidden-import "PySide6.QtNetwork" ^
    --hidden-import "PIL" ^
    --hidden-import "pandas" ^
    --hidden-import "reportlab" ^
    --hidden-import "openpyxl" ^
    --hidden-import "requests" ^
    --hidden-import "dotenv" ^
    --noconfirm

REM Optional: Code signing (uncomment when you have a certificate)
REM signtool sign /fd SHA256 /f "path\to\certificate.pfx" /p "password" /tr "http://timestamp.digicert.com" /td SHA256 "dist\CyberToolsSuite\CyberToolsSuite.exe"

echo.
echo ============================================================
echo Build complete!
echo ============================================================
echo.
echo Your app is at: dist\CyberToolsSuite\CyberToolsSuite.exe
echo.
echo Next steps:
echo 1. Run installer\setup.iss with Inno Setup to make an installer
echo 2. (Optional) Sign the installer with your code signing certificate
echo.
echo ============================================================
echo Copyright (c) 2026 CyberTools. All Rights Reserved.
echo ============================================================
pause