# Sync Qt Designer editing package (repo StockTracker-Designer and/or Desktop copy).
param(
    [ValidateSet("Repo", "Desktop", "All")]
    [string]$Target = "All"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

& (Join-Path $Root ".venv\Scripts\python.exe") (Join-Path $Root "tools\generate_all_designer_uis.py") 2>$null
if (-not $?) {
    python (Join-Path $Root "tools\generate_all_designer_uis.py")
}

function Sync-ToDesignerFolder($Designer) {
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

    $equipmentsUi = Join-Path $Root "src\gui\designer\gui_equipments.ui"
    if (Test-Path $equipmentsUi) {
        Copy-UiForDesigner $equipmentsUi (Join-Path $Designer "gui_equipments.ui")
    }

    $popSrc = Join-Path $Root "src\gui\designer\popups"
    $popDest = Join-Path $Designer "popups"
    if (Test-Path $popDest) {
        Get-ChildItem $popDest -Filter "gui_popup_*.ui" -File -ErrorAction SilentlyContinue |
            ForEach-Object { Remove-Item $_.FullName -Force }
    }
    Get-ChildItem $popSrc -Filter "*.ui" -Recurse | ForEach-Object {
        $rel = $_.FullName.Substring($popSrc.Length + 1)
        $destPath = Join-Path $popDest $rel
        New-Item -ItemType Directory -Force -Path (Split-Path $destPath) | Out-Null
        Copy-Item $_.FullName $destPath -Force
    }
    Copy-Item (Join-Path $popSrc "README.md") (Join-Path $popDest "README.md") -Force -ErrorAction SilentlyContinue

    $st = Join-Path $Root "src\gui\siemens_template"
    $stDest = Join-Path $Designer "siemens_template"
    if (Test-Path (Join-Path $Designer "siemens_templates")) {
        Remove-Item (Join-Path $Designer "siemens_templates") -Recurse -Force
    }
    robocopy $st $stDest /E /NFL /NDL /NJH /NJS | Out-Null

    $designerBat = Join-Path $Root "tools\DESIGNER-DESKTOP.bat"
    if (Test-Path $designerBat) {
        Copy-Item $designerBat (Join-Path $Designer "DESIGNER.bat") -Force
    }
    Copy-Item (Join-Path $Root "src\gui\designer\README.md") (Join-Path $Designer "README.md") -Force -ErrorAction SilentlyContinue
    Copy-Item (Join-Path $Root "src\gui\designer\popups\README.md") (Join-Path $Designer "popups\README.md") -Force -ErrorAction SilentlyContinue
    $leiaMe = Join-Path $Root "StockTracker-Designer\LEIA-ME.txt"
    $leiaMeDest = Join-Path $Designer "LEIA-ME.txt"
    if ((Test-Path $leiaMe) -and ((Resolve-Path $leiaMe).Path -ne (Resolve-Path $leiaMeDest -ErrorAction SilentlyContinue).Path)) {
        Copy-Item $leiaMe $leiaMeDest -Force
    }
    $equipmentsReadme = Join-Path $Root "src\gui\designer\EQUIPMENTS-LEIA-ME.txt"
    if (Test-Path $equipmentsReadme) {
        Copy-Item $equipmentsReadme (Join-Path $Designer "EQUIPMENTS-LEIA-ME.txt") -Force
    }

    Write-Host "Designer package ready: $Designer"
}

if ($Target -eq "Repo" -or $Target -eq "All") {
    Sync-ToDesignerFolder (Join-Path $Root "StockTracker-Designer")
}
if ($Target -eq "Desktop" -or $Target -eq "All") {
    Sync-ToDesignerFolder (Join-Path $env:USERPROFILE "Desktop\StockTracker-Designer")
}
