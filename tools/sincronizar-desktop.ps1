# Copy project to Desktop\StockTracker-Projeto (backup / tutor). Skips secrets and venv.
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Dest = Join-Path $env:USERPROFILE "Desktop\StockTracker-Projeto"

Write-Host "Sync: $Root"
Write-Host "  -> $Dest"

New-Item -ItemType Directory -Force -Path $Dest | Out-Null
robocopy $Root $Dest /E /XD .venv __pycache__ .git /XF secrets.py /NFL /NDL /NJH /NJS | Out-Null
if ($LASTEXITCODE -ge 8) { exit $LASTEXITCODE }

# Designer package (ui paths fixed for Desktop layout)
& (Join-Path $Root "tools\prepare-designer-desktop.ps1")

Write-Host "Done."
Write-Host "  Project copy: $Dest"
Write-Host "  Designer:     $env:USERPROFILE\Desktop\StockTracker-Designer"
