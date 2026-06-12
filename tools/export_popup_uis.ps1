# Regenerate Python from popup .ui files (after editing in Qt Designer).
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Popups = Join-Path $Root "src\gui\designer\popups"

$Uic = Join-Path $Root ".venv\Scripts\pyside6-uic.exe"
if (-not (Test-Path $Uic)) { $Uic = "pyside6-uic" }

Get-ChildItem $Popups -Filter "*.ui" -Recurse | ForEach-Object {
    $py = Join-Path $_.DirectoryName ($_.BaseName + ".py")
    & $Uic $_.FullName -o $py
    Write-Host "Exported: $py"
}

Write-Host "Dialogs import from src/gui/designer/popups/{components,materials,shared}/"
