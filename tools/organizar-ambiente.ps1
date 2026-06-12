# Organiza projeto + pacotes Qt Designer (repo, Desktop Designer, Desktop Projeto).
# Inclui pagina Materials (gui_materials.ui).
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Desktop = [Environment]::GetFolderPath("Desktop")
$DesignerRepo = Join-Path $Root "StockTracker-Designer"
$DesignerDesktop = Join-Path $Desktop "StockTracker-Designer"
$ProjetoDesktop = Join-Path $Desktop "StockTracker-Projeto"

Write-Host ""
Write-Host "=== Stock Tracker - organizar ambiente ===" -ForegroundColor Cyan
Write-Host ""

# 1) Regenerar .ui canonicos (Components + Materials + popups)
Write-Host "[1/4] Gerar .ui a partir dos templates..." -ForegroundColor Yellow
& (Join-Path $Root ".venv\Scripts\python.exe") (Join-Path $Root "tools\generate_all_designer_uis.py") 2>$null
if (-not $?) { python (Join-Path $Root "tools\generate_all_designer_uis.py") }

# 2) Exportar .ui -> .py (app)
Write-Host "[2/4] Exportar .ui para Python..." -ForegroundColor Yellow
& (Join-Path $PSScriptRoot "export_designer_uis.ps1")

# 3) Sincronizar pacotes Designer (repo + Ambiente de Trabalho)
Write-Host "[3/4] Sincronizar StockTracker-Designer..." -ForegroundColor Yellow
& (Join-Path $PSScriptRoot "sync_designer_package.ps1") -Target All

# 4) Copia completa do projeto para Desktop\StockTracker-Projeto
Write-Host "[4/4] Sincronizar Desktop\StockTracker-Projeto..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $ProjetoDesktop | Out-Null
robocopy $Root $ProjetoDesktop /E /XD .venv __pycache__ .git /XF secrets.py /NFL /NDL /NJH /NJS | Out-Null
if ($LASTEXITCODE -ge 8) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "=== Verificacao ===" -ForegroundColor Cyan

$checks = @(
    @{ Label = "Repo: gui_materials.ui";           Path = Join-Path $Root "src\gui\designer\gui_materials.ui" },
    @{ Label = "Repo: materials_page.py";           Path = Join-Path $Root "src\gui\materials_page.py" },
    @{ Label = "Designer (repo): gui_materials.ui"; Path = Join-Path $DesignerRepo "gui_materials.ui" },
    @{ Label = "Designer (Desktop): gui_materials.ui"; Path = Join-Path $DesignerDesktop "gui_materials.ui" },
    @{ Label = "Desktop Projeto: materials";        Path = Join-Path $ProjetoDesktop "src\gui\designer\gui_materials.ui" },
    @{ Label = "Designer (Desktop): DESIGNER.bat";  Path = Join-Path $DesignerDesktop "DESIGNER.bat" }
)

$ok = $true
foreach ($c in $checks) {
    $exists = Test-Path $c.Path
    if (-not $exists) { $ok = $false }
    $mark = if ($exists) { "OK" } else { "FALTA" }
    $color = if ($exists) { "Green" } else { "Red" }
    Write-Host ("  [{0}] {1}" -f $mark, $c.Label) -ForegroundColor $color
}

Write-Host ""
Write-Host "Pastas:" -ForegroundColor Cyan
Write-Host "  Projeto (Git):     $Root"
Write-Host "  Qt Designer:       $DesignerDesktop"
Write-Host "  Copia Desktop:     $ProjetoDesktop"
Write-Host ""
Write-Host "Qt Designer - Materials: duplo-clique em" -ForegroundColor Cyan
Write-Host "  $DesignerDesktop\DESIGNER.bat" -ForegroundColor White
Write-Host "  Opcao 2 = gui_materials.ui"
Write-Host ""

if (-not $ok) {
    Write-Host "Alguns ficheiros em falta - reveja os erros acima." -ForegroundColor Red
    exit 1
}

Write-Host "Ambiente organizado." -ForegroundColor Green
