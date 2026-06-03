# Repository layout

## Overview

| Directory | Purpose |
|-----------|---------|
| `src/core/` | Business logic (`StockTracker`, supplier APIs) |
| `src/gui/` | PySide6 application UI |
| `src/gui/siemens_template/` | Official Siemens UI templates and resources |
| `data/` | Local Excel database (`stock.xlsx`) |
| `config/` | Local credentials (`secrets.py`, not in Git) |
| `docs/` | Project documentation |
| `tools/` | Maintenance scripts (UI export, sync, doc generation) |
| `scripts/` | Standalone test utilities |

---

## Source code (`src/`)

| File | Role |
|------|------|
| `main.py` | Application entry point (GUI) |
| `test_terminal.py` | Terminal test console (development) |
| `core/stock.py` | `StockTracker` — Excel, stock movements, catalog lookup |
| `gui/stock_tracker_window.py` | Main window and event handlers |
| `gui/designer/gui_stocktracker.ui` | Main layout (Qt Designer) |
| `gui/designer/gui_stocktracker.py` | Generated UI module (do not edit by hand) |
| `gui/history_dialog.py` | History viewer dialog |
| `gui/styles.py` | Siemens visual styling |

---

## Configuration

1. Copy `config/secrets.example.py` to `config/secrets.py`
2. Set API keys for the suppliers you use
3. Place or update `data/stock.xlsx`
4. Close Excel before the application saves the workbook

---

## How to run

| Correct | Incorrect |
|---------|-----------|
| `python -m src.main` | `python src/gui/history_dialog.py` |
| `run.bat` | Running GUI modules with relative imports in isolation |

Always run from the **repository root** (directory that contains `src/`, `config/`, and `run.bat`).

---

## Legacy reference

An older implementation may exist outside this repository. Use **only this repo** as the maintained codebase; do not mix files from legacy copies.

---

## Optional workspace copy

To mirror the project to another folder (backup or second machine), use:

```powershell
.\tools\sincronizar-desktop.ps1
```

The script does not copy `config/secrets.py` or `.venv/`. See [WORKSPACE.md](WORKSPACE.md) if present, or `tools/README.md`.
