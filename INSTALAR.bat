@echo off
title Stock Tracker - Instalacao
cd /d "%~dp0"

echo.
echo === Stock Tracker - Instalacao ===
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado. Instale Python 3.10+ de python.org
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo A criar ambiente virtual...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar .venv
        pause
        exit /b 1
    )
)

echo A instalar dependencias...
".venv\Scripts\python.exe" -m pip install -q --upgrade pip
".venv\Scripts\python.exe" -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERRO] Falha no pip install
    pause
    exit /b 1
)

if not exist "config\secrets.py" (
    copy "config\secrets.example.py" "config\secrets.py" >nul
    echo Criado config\secrets.py - edite com as chaves API.
)

echo.
echo Instalacao concluida. Execute run.bat
echo Manual: docs\guias\MANUAL_UTILIZADOR.md
echo.
pause
