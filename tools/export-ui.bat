@echo off
REM Apos editar .ui no Qt Designer, corre isto (exporta janela + materials + popups).
cd /d "%~dp0.."
set "PY=%~dp0..\.venv\Scripts\python.exe"
set "UIC=%~dp0..\.venv\Scripts\pyside6-uic.exe"
if not exist "%UIC%" (
    echo [ERRO] pyside6-uic nao encontrado. pip install -r requirements.txt
    pause
    exit /b 1
)
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\export_designer_uis.ps1"
pause
