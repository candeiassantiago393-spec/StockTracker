# Open Qt Designer — Components or Materials (.ui in src/gui/designer).
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$DesignerDir = Join-Path $Root "src\gui\designer"

$Uic = "pyside6-designer"
$VenvDesigner = Join-Path $Root ".venv\Scripts\pyside6-designer.exe"
if (Test-Path $VenvDesigner) { $Uic = $VenvDesigner }

$files = @{
    "1" = @{ Name = "Components (gui_stocktracker.ui)"; Path = Join-Path $DesignerDir "gui_stocktracker.ui" }
    "2" = @{ Name = "Materials (gui_materials.ui)";     Path = Join-Path $DesignerDir "gui_materials.ui" }
}

Write-Host ""
Write-Host "Stock Tracker — Qt Designer (repo)"
Write-Host "  1 - Components   gui_stocktracker.ui"
Write-Host "  2 - Materials    gui_materials.ui"
Write-Host ""
$choice = Read-Host "Opcao [1-2, Enter=1]"
if ([string]::IsNullOrWhiteSpace($choice)) { $choice = "1" }
if (-not $files.ContainsKey($choice)) {
    Write-Error "Opcao invalida: $choice"
}

$target = $files[$choice]
if (-not (Test-Path $target.Path)) {
    Write-Error "Ficheiro em falta: $($target.Path)`nCorre: python tools\generate_all_designer_uis.py"
}

Write-Host "A abrir: $($target.Name)"
Start-Process $Uic -ArgumentList "`"$($target.Path)`""
