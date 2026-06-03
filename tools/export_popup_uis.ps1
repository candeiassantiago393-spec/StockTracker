# Regenerate Python from popup .ui files (after editing in Qt Designer).
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Popups = Join-Path $Root "src\gui\designer\popups"
$Out = Join-Path $Root "src\gui\designer\popups"

Get-ChildItem $Popups -Filter "*.ui" | ForEach-Object {
    $py = Join-Path $Out ($_.BaseName + ".py")
    pyside6-uic $_.FullName -o $py
    Write-Host "Exported: $py"
}

Write-Host "Dialogs import from src/gui/designer/popups/gui_popup_*.py"
