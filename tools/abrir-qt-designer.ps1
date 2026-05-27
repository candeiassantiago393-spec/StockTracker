# Open gui_stocktracker.ui in Qt Designer (correct path for resources.qrc).
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Ui = Join-Path $Root "src\gui\designer\gui_stocktracker.ui"
if (-not (Test-Path $Ui)) {
    Write-Error "UI file not found: $Ui"
}
Write-Host "Opening: $Ui"
Start-Process pyside6-designer -ArgumentList "`"$Ui`""
