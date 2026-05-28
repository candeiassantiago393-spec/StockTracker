@echo off
title Stock Tracker - Qt Designer
cd /d "%~dp0"

set "DESIGNER=pyside6-designer"
set "VENV_UI=%USERPROFILE%\Desktop\StockTracker-Projeto\.venv\Scripts\pyside6-designer.exe"
set "VENV_UI2=%USERPROFILE%\Downloads\StockTracker\StockTracker\.venv\Scripts\pyside6-designer.exe"

if exist "%VENV_UI%" set "DESIGNER=%VENV_UI%"
if exist "%VENV_UI2%" set "DESIGNER=%VENV_UI2%"

if not exist "%DESIGNER%" (
    where pyside6-designer >nul 2>&1
    if errorlevel 1 (
        echo [ERRO] pyside6-designer nao encontrado.
        echo.
        echo Instale PySide6 no .venv do projeto:
        echo   pip install PySide6
        echo.
        pause
        exit /b 1
    )
    set "DESIGNER=pyside6-designer"
)

echo.
echo  Stock Tracker - Qt Designer
echo  Pasta: %~dp0
echo  Designer: %DESIGNER%
echo.
echo  1 - Janela principal          gui_stocktracker.ui
echo  2 - Popup manual              popups\gui_popup_manual.ui
echo  3 - Popup historico           popups\gui_popup_history.ui
echo  4 - Popup pesquisa            popups\gui_popup_search.ui
echo  5 - Template Siemens base     popups\gui_popup_template.ui
echo.
set /p OPCAO=Opcao [1-5, Enter=1]: 
if "%OPCAO%"=="" set OPCAO=1

if "%OPCAO%"=="1" goto main
if "%OPCAO%"=="2" goto manual
if "%OPCAO%"=="3" goto history
if "%OPCAO%"=="4" goto search
if "%OPCAO%"=="5" goto template
echo Opcao invalida.
pause
exit /b 1

:main
set "FILE=%~dp0gui_stocktracker.ui"
goto open

:manual
set "FILE=%~dp0popups\gui_popup_manual.ui"
goto open

:history
set "FILE=%~dp0popups\gui_popup_history.ui"
goto open

:search
set "FILE=%~dp0popups\gui_popup_search.ui"
goto open

:template
set "FILE=%~dp0popups\gui_popup_template.ui"
goto open

:open
if not exist "%FILE%" (
    echo [ERRO] Ficheiro em falta:
    echo   %FILE%
    echo.
    echo No projeto Downloads execute:
    echo   python tools\generate_popup_uis.py
    echo   powershell -File tools\prepare-designer-desktop.ps1
    pause
    exit /b 1
)
echo A abrir: %FILE%
"%DESIGNER%" "%FILE%"
if errorlevel 1 (
    echo.
    echo [ERRO] Qt Designer nao abriu o ficheiro.
    pause
)
exit /b 0
