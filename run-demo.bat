@echo off
title Stock Tracker - Demo (legacy UI)
cd /d "%~dp0"
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo Aviso: .venv nao encontrado. A usar Python global.
)
echo.
echo  Stock Tracker DEMO - interface antiga
echo  Verde = ADD STOCK   Vermelho = REMOVE STOCK
echo  (versao antes do template Siemens final)
echo.
python -m src.main_demo
if errorlevel 1 pause
