@echo off
title Stock Tracker - Qt Designer
cd /d "%~dp0"

where pyside6-designer >nul 2>&1
if errorlevel 1 (
    echo [ERRO] pyside6-designer nao encontrado.
    echo.
    echo No projeto principal:
    echo   cd Downloads\StockTracker\StockTracker
    echo   .\.venv\Scripts\activate
    echo   pip install PySide6
    echo.
    pause
    exit /b 1
)

echo.
echo  Stock Tracker - Qt Designer
echo  Pasta: %~dp0
echo.
echo  1 - Janela principal     (gui_stocktracker.ui)
echo  2 - Popup manual         (popups\gui_popup_manual.ui)
echo  3 - Popup historico      (popups\gui_popup_history.ui)
echo  4 - Popup pesquisa       (popups\gui_popup_search.ui)
echo.
set /p OPCAO=Opcao [1-4, Enter=1]: 
if "%OPCAO%"=="" set OPCAO=1

if "%OPCAO%"=="1" goto main
if "%OPCAO%"=="2" goto manual
if "%OPCAO%"=="3" goto history
if "%OPCAO%"=="4" goto search
echo Opcao invalida.
pause
exit /b 1

:main
if not exist "%~dp0gui_stocktracker.ui" (
    echo [ERRO] Ficheiro em falta: gui_stocktracker.ui
    echo Execute no projeto: tools\prepare-designer-desktop.ps1
    pause
    exit /b 1
)
start "" pyside6-designer "%~dp0gui_stocktracker.ui"
goto end

:manual
start "" pyside6-designer "%~dp0popups\gui_popup_manual.ui"
goto end

:history
start "" pyside6-designer "%~dp0popups\gui_popup_history.ui"
goto end

:search
start "" pyside6-designer "%~dp0popups\gui_popup_search.ui"
goto end

:end
exit /b 0
