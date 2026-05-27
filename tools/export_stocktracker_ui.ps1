# Regenerate Python UI from Qt Designer file (run after editing gui_stocktracker.ui).
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$UiFile = Join-Path $Root "src\gui\designer\gui_stocktracker.ui"
$PyFile = Join-Path $Root "src\gui\designer\gui_stocktracker.py"

pyside6-uic $UiFile -o $PyFile

$content = Get-Content $PyFile -Raw
$content = $content.Replace(
    "import resources_rc",
    "from src.gui.siemens_template.resources import resources_rc"
)
Set-Content $PyFile $content -Encoding UTF8

Write-Host "Exported: $PyFile"
Write-Host "Restart the app: python -m src.main"
