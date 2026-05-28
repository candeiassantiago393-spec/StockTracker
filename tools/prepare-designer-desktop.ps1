# Build Desktop\StockTracker-Designer (gui + popups + siemens_template + DESIGNER.bat).
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Designer = Join-Path $env:USERPROFILE "Desktop\StockTracker-Designer"

& (Join-Path $Root ".venv\Scripts\python.exe") (Join-Path $Root "tools\generate_stocktracker_ui.py") 2>$null
if (-not $?) {
    python (Join-Path $Root "tools\generate_stocktracker_ui.py")
}
python (Join-Path $Root "tools\generate_popup_uis.py")

New-Item -ItemType Directory -Force -Path $Designer | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $Designer "popups") | Out-Null

function Copy-UiForDesigner($src, $dest) {
    $text = Get-Content $src -Raw -Encoding UTF8
    $text = $text.Replace("../siemens_template/", "siemens_template/")
    Set-Content $dest $text -Encoding UTF8 -NoNewline
}

Copy-UiForDesigner `
    (Join-Path $Root "src\gui\designer\gui_stocktracker.ui") `
    (Join-Path $Designer "gui_stocktracker.ui")

$popSrc = Join-Path $Root "src\gui\designer\popups"
Get-ChildItem $popSrc -Filter "*.ui" | ForEach-Object {
    Copy-Item $_.FullName (Join-Path (Join-Path $Designer "popups") $_.Name) -Force
}

$st = Join-Path $Root "src\gui\siemens_template"
$stDest = Join-Path $Designer "siemens_template"
robocopy $st $stDest /E /NFL /NDL /NJH /NJS | Out-Null

Copy-Item (Join-Path $Root "tools\DESIGNER-DESKTOP.bat") (Join-Path $Designer "DESIGNER.bat") -Force
Copy-Item (Join-Path $Root "src\gui\designer\popups\README.md") (Join-Path $Designer "popups\README.md") -Force -ErrorAction SilentlyContinue
Copy-Item (Join-Path $Root "Desktop-Designer-LEIA-ME.txt") (Join-Path $Designer "LEIA-ME.txt") -Force

Write-Host "Designer package ready: $Designer"
