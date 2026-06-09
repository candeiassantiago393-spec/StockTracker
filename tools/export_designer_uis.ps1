# Export all designer .ui files to Python (run after editing in Qt Designer).
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$DesignerDir = Join-Path $Root "src\gui\designer"

$Uic = Join-Path $Root ".venv\Scripts\pyside6-uic.exe"
if (-not (Test-Path $Uic)) { $Uic = "pyside6-uic" }

$MainUi = Join-Path $DesignerDir "gui_stocktracker.ui"
$MainPy = Join-Path $DesignerDir "gui_stocktracker.py"
& $Uic $MainUi -o $MainPy
$content = Get-Content $MainPy -Raw
$content = $content.Replace(
    "import resources_rc",
    "from src.gui.siemens_template.resources import resources_rc"
)
Set-Content $MainPy $content -Encoding UTF8
Write-Host "Exported: $MainPy"

$MaterialsUi = Join-Path $DesignerDir "gui_materials.ui"
$MaterialsPy = Join-Path $DesignerDir "gui_materials.py"
if (Test-Path $MaterialsUi) {
    & $Uic $MaterialsUi -o $MaterialsPy
    Write-Host "Exported: $MaterialsPy"
}

& (Join-Path $PSScriptRoot "export_popup_uis.ps1")

Write-Host "Done. Restart: python -m src.main"
