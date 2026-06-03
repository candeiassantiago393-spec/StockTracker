---
description: Stock Tracker — architecture and conventions
globs:
  - "**/*"
alwaysApply: true
---

# Stock Tracker

## Architecture

- Business logic: `src/core/stock.py` (`StockTracker`)
- GUI: `src/gui/stock_tracker_window.py`
- Entry: `python -m src.main` or `run.bat` (single GUI; SCAN queries all configured suppliers)
- Credentials: `config/secrets.py` (never commit)
- Data: `data/stock.xlsx` — close Excel before saving

## Rules

- No business logic in the GUI layer
- Do not run `gui/` modules in isolation (relative imports)
- Minimal diffs; match existing style
- Documentation: English in `docs/user/`; spec also in `docs/PROJETO_STOCKTRACKER.md`
