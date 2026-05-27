# Copy project to Desktop\StockTracker-Projeto (backup / tutor). Skips secrets and venv.
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Dest = Join-Path $env:USERPROFILE "Desktop\StockTracker-Projeto"

Write-Host "Sync: $Root"
Write-Host "  -> $Dest"

New-Item -ItemType Directory -Force -Path $Dest | Out-Null
robocopy $Root $Dest /E /XD .venv __pycache__ .git /XF secrets.py /NFL /NDL /NJH /NJS | Out-Null
if ($LASTEXITCODE -ge 8) { exit $LASTEXITCODE }

# Designer package (ui + resources for tutor)
$Designer = Join-Path $env:USERPROFILE "Desktop\StockTracker-Designer"
New-Item -ItemType Directory -Force -Path $Designer | Out-Null
Copy-Item (Join-Path $Root "src\gui\designer\gui_stocktracker.ui") (Join-Path $Designer "gui_stocktracker.ui") -Force
$st = Join-Path $Root "src\gui\siemens_template"
$stDest = Join-Path $Designer "siemens_template"
robocopy $st $stDest /E /NFL /NDL /NJH /NJS | Out-Null

Write-Host "Done."
Write-Host "  Project copy: $Dest"
Write-Host "  Designer UI:  $Designer\gui_stocktracker.ui"
