@echo off
title Stock Tracker - organizar ambiente
cd /d "%~dp0.."
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0organizar-ambiente.ps1"
echo.
pause
