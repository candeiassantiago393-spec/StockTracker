@echo off
title Stock Tracker
cd /d "%~dp0"

set "PY=%~dp0.venv\Scripts\python.exe"
if not exist "%PY%" (
    echo [ERRO] Ambiente virtual nao encontrado.
    echo Execute: python -m venv .venv
    echo Depois: .\.venv\Scripts\activate
    echo         pip install -r requirements.txt
    pause
    exit /b 1
)

"%PY%" -m pip install -q -r "%~dp0requirements.txt" 2>nul
"%PY%" -m src.main
if errorlevel 1 (
    echo.
    echo [ERRO] A aplicacao terminou com erro.
    pause
)
