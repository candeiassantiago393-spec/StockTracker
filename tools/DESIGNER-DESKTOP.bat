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
        echo   pip install PySide6
        pause
        exit /b 1
    )
    set "DESIGNER=pyside6-designer"
)

echo.
echo  Stock Tracker - Qt Designer
echo  Pasta: %~dp0
echo.
echo  Paginas principais
echo    1 - Components     gui_stocktracker.ui
echo    2 - Equipments     gui_equipments.ui
echo.
echo  Popups Components  (popups\components\)
echo    3 - Manual         gui_popup_manual.ui
echo    4 - Editar         gui_popup_edit.ui
echo    5 - Pesquisa       gui_popup_search.ui
echo    6 - Historico      gui_popup_history.ui
echo.
echo  Popups Equipments  (popups\equipments\)
echo    7 - Equipment      gui_popup_equipment.ui
echo    8 - Pesquisa       gui_popup_search.ui
echo    9 - Historico      gui_popup_history.ui
echo.
echo  Partilhados        (popups\shared\)
echo   10 - Confirmacao    gui_popup_confirm.ui
echo   11 - Template       gui_popup_template.ui
echo.
set /p OPCAO=Opcao [1-11, Enter=1]: 
if "%OPCAO%"=="" set OPCAO=1

if "%OPCAO%"=="1"  set "FILE=%~dp0gui_stocktracker.ui" & goto open
if "%OPCAO%"=="2"  set "FILE=%~dp0gui_equipments.ui" & goto open
if "%OPCAO%"=="3"  set "FILE=%~dp0popups\components\gui_popup_manual.ui" & goto open
if "%OPCAO%"=="4"  set "FILE=%~dp0popups\components\gui_popup_edit.ui" & goto open
if "%OPCAO%"=="5"  set "FILE=%~dp0popups\components\gui_popup_search.ui" & goto open
if "%OPCAO%"=="6"  set "FILE=%~dp0popups\components\gui_popup_history.ui" & goto open
if "%OPCAO%"=="7"  set "FILE=%~dp0popups\equipments\gui_popup_equipment.ui" & goto open
if "%OPCAO%"=="8"  set "FILE=%~dp0popups\equipments\gui_popup_search.ui" & goto open
if "%OPCAO%"=="9"  set "FILE=%~dp0popups\equipments\gui_popup_history.ui" & goto open
if "%OPCAO%"=="10" set "FILE=%~dp0popups\shared\gui_popup_confirm.ui" & goto open
if "%OPCAO%"=="11" set "FILE=%~dp0popups\shared\gui_popup_template.ui" & goto open
echo Opcao invalida.
pause
exit /b 1

:open
if not exist "%FILE%" (
    echo [ERRO] Ficheiro em falta: %FILE%
    echo Execute tools\ORGANIZAR-DESKTOP.bat no projeto.
    pause
    exit /b 1
)
echo A abrir: %FILE%
"%DESIGNER%" "%FILE%"
exit /b 0
