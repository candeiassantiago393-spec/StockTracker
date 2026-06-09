# Build Desktop\StockTracker-Designer (gui + popups + siemens_template + DESIGNER.bat).
$ErrorActionPreference = "Stop"
& (Join-Path $PSScriptRoot "sync_designer_package.ps1") -Target Desktop
