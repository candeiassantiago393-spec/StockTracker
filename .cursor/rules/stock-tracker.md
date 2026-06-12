---
description: Stock Tracker — architecture and conventions
globs:
  - "**/*"
alwaysApply: true
---

# Stock Tracker

Raiz: `C:\Users\z005027j\Downloads\StockTracker\StockTracker`

## Arquitetura

- Lógica: `src/core/stock.py` (classe `StockTracker` — Components, Materials, History)
- GUI Components: `src/gui/stock_tracker_window.py` + `designer/gui_stocktracker.ui`
- GUI Materials: `src/gui/materials_page.py` + `designer/gui_materials.ui`
- Entrada: `python -m src.main` ou `run.bat`
- Credenciais: `config/secrets.py` (não commitar)
- Dados: `data/stock.xlsx` — fechar Excel antes de gravar

## Qt Designer

- Canónico: `src/gui/designer/`
- Pacote edição: `StockTracker-Designer/` (repo) e `Desktop\StockTracker-Designer`
- Sincronizar: `ORGANIZAR-DESKTOP.bat`
- Métricas template: `src/gui/styles.py`, `tools/gui_ui_builder.py`
- Guia Materials (PT): `src/gui/designer/MATERIALS-LEIA-ME.txt`

## Regras

- Não colocar lógica de negócio na GUI
- Não executar módulos `gui/` isoladamente (imports relativos)
- Diffs minimos; estilo existente
- Documentação EN em `docs/user/`; guia PT em `docs/GUIA_RAPIDO_PT.md`

## Não confundir

`Documents\stock-tracker` — projeto legado separado.
