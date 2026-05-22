@echo off
cd /d "%~dp0\.."
echo A organizar templates Siemens em src\gui\siemens_template\ ...
echo.

set "PY=%~dp0..\.venv\Scripts\python.exe"
if not exist "%PY%" (
    echo ERRO: .venv nao encontrado.
    pause
    exit /b 1
)

"%PY%" "%~dp0reorganize_gui_template.py"
echo.
echo Concluido. Ver src\gui no Explorer.
pause
