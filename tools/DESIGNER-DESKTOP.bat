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
echo  1 - Janela principal (Components)  gui_stocktracker.ui
echo  2 - Pagina Materials              gui_materials.ui
echo  3 - Popup manual                  popups\gui_popup_manual.ui
echo  4 - Popup historico               popups\gui_popup_history.ui
echo  5 - Popup pesquisa                popups\gui_popup_search.ui
echo  6 - Template Siemens base         popups\gui_popup_template.ui
echo  7 - Popup editar componente       popups\gui_popup_edit.ui
echo  8 - Popup confirmacao             popups\gui_popup_confirm.ui
echo.
set /p OPCAO=Opcao [1-8, Enter=1]: 
if "%OPCAO%"=="" set OPCAO=1

if "%OPCAO%"=="1" goto main
if "%OPCAO%"=="2" goto materials
if "%OPCAO%"=="3" goto manual
if "%OPCAO%"=="4" goto history
if "%OPCAO%"=="5" goto search
if "%OPCAO%"=="6" goto template
if "%OPCAO%"=="7" goto edit
if "%OPCAO%"=="8" goto confirm
echo Opcao invalida.
pause
exit /b 1

:main
set "FILE=%~dp0gui_stocktracker.ui"
goto open

:materials
set "FILE=%~dp0gui_materials.ui"
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

:edit
set "FILE=%~dp0popups\gui_popup_edit.ui"
goto open

:confirm
set "FILE=%~dp0popups\gui_popup_confirm.ui"
goto open

:open
if not exist "%FILE%" (
    echo [ERRO] Ficheiro em falta:
    echo   %FILE%
    echo.
    echo No projeto execute:
    echo   python tools\generate_all_designer_uis.py
    echo   powershell -File tools\sync_designer_package.ps1
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
