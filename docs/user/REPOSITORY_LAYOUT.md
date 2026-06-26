# Repository layout

## Overview

| Directory | Purpose |
|-----------|---------|
| `src/core/` | Business logic (`StockTracker`, supplier APIs) |
| `src/gui/` | PySide6 application UI |
| `src/gui/designer/` | Canonical Qt Designer `.ui` + exported `.py` |
| `src/gui/siemens_template/` | Siemens UI templates, icons, fonts |
| `StockTracker-Designer/` | Designer editing package (mirror of `.ui` + resources; see `LEIA-ME.txt`) |
| `data/` | Local Excel database (`stock.xlsx`) |
| `config/` | Local credentials (`secrets.py`, not in Git) |
| `docs/` | Project documentation |
| `docs/especificacao/` | Product specification (EN + PT) |
| `docs/guias/` | Portuguese quick guides |
| `docs/designer/` | Qt Designer documentation index |
| `docs/fluxogramas/` | Flowcharts (Mermaid) per app area |
| `docs/roadmap/` | Suggested improvements |
| `tools/` | Maintenance scripts (UI export, sync, doc generation) |
| `scripts/` | Standalone test utilities |

---

## Source code (`src/`)

| File | Role |
|------|------|
| `main.py` | Application entry point (GUI) |
| `test_terminal.py` | Terminal test console (development) |
| `core/stock.py` | `StockTracker` — Excel, components, equipments, history, APIs |
| `gui/stock_tracker_window.py` | Main window, Components page, navigation |
| `gui/equipments_page.py` | Equipments page logic |
| `gui/designer/gui_stocktracker.ui` | Components layout (Qt Designer) |
| `gui/designer/gui_equipments.ui` | Equipments layout (Qt Designer) |
| `gui/designer/gui_*.py` | Generated UI modules (do not edit by hand) |
| `gui/styles.py` | Siemens metrics and styles |
| `gui/*_dialog.py` | Popup behaviour on top of `designer/popups/` |

GUI map (Portuguese): [src/gui/ESTRUTURA.md](../../src/gui/ESTRUTURA.md)

---

## Root-level helpers

| File | Role |
|------|------|
| `run.bat` | Start the GUI |
| `tools/ORGANIZAR-DESKTOP.bat` | Sync Designer packages + Desktop project copy |

---

## Configuration

1. Copy `config/secrets.example.py` to `config/secrets.py`
2. Set API keys for the suppliers you use
3. Place or update `data/stock.xlsx` (sheets: Components, Equipments, History)
4. Close Excel before the application saves the workbook

---

## How to run

| Correct | Incorrect |
|---------|-----------|
| `python -m src.main` | `python src/gui/history_dialog.py` |
| `run.bat` | Running GUI modules with relative imports in isolation |

Always run from the **repository root** (directory that contains `src/`, `config/`, and `run.bat`).

---

## Optional Desktop copies

```powershell
tools\ORGANIZAR-DESKTOP.bat
```

Creates/updates:

- `Desktop\StockTracker-Designer` — Qt Designer only
- `Desktop\StockTracker-Projeto` — full project copy (no `.git`, no `secrets.py`, no `.venv`)

See [WORKSPACE.md](WORKSPACE.md).

---

## Legacy reference

An older implementation may exist outside this repository. Use **only this repo** as the maintained codebase.
