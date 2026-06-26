# Stock Tracker

**Desktop electronic component inventory with Siemens-style UI.**

Stock management using a local Excel database, PySide6 GUI, and optional distributor API integration (Mouser, DigiKey, TME, RS, and extensible suppliers).

> Full documentation: [`docs/README.md`](docs/README.md) — specification: [EN](docs/especificacao/PROJETO_STOCKTRACKER.md) · [PT](docs/especificacao/PROJETO_STOCKTRACKER_PT.md)

---

## Features

- Excel inventory (`Components`, `Equipments`, and `History` sheets)
- GUI: **Components** (search, barcode/scan, stock IN/OUT) and **Equipments** (calibrated items)
- Header navigation COMPONENTS / EQUIPMENTS with shared action bar
- Multi-match Excel search with selection dialog
- Autocomplete from Excel (search and barcode fields)
- Mouser API: catalog lookup and import
- **Component catalog image** (Mouser `/lrg/` resolution) with hover magnifier, wheel zoom, and **bounded local cache** (`data/component_image_cache/`)
- **Equipment images** — drag & drop or Add/Delete, stored in `data/equipments/{id}/`
- **Multi-distributor SCAN**: queries configured APIs in order until a match is found
- Modular suppliers under `src/core/suppliers/`
- Optional terminal test menu: `python -m src.test_terminal`
- Clear separation: business logic in `core/`, UI in `gui/`

---

## Requirements

- Windows 10/11
- Python 3.10+
- Network access for distributor APIs (as configured)
- Close `data/stock.xlsx` in Excel before saving from the application

---

## Quick start

```powershell
git clone https://github.com/candeiassantiago393-spec/StockTracker.git
cd StockTracker
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy config\secrets.example.py config\secrets.py
```

1. Edit `config/secrets.py` — set API keys for the suppliers you use.
2. Add or create `data/stock.xlsx` (see [`data/README.md`](data/README.md)).
3. Run:

```powershell
python -m src.main
```

Or double-click `run.bat`.

---

## Configuration

| File | Purpose |
|------|---------|
| `config/secrets.py` | API keys (**local only**, not in Git) |
| `config/secrets.example.py` | Credential template |
| `data/stock.xlsx` | Inventory database (**gitignored** by default) |

Never commit `config/secrets.py` or real API keys.

---

## Project structure

```
StockTracker/
├── config/                 # credentials loader + secrets.example.py
├── data/                   # stock.xlsx (local) + backups/ + image caches
├── docs/                   # documentation (EN + PT quick guide)
├── StockTracker-Designer/  # Qt Designer package (.ui + LEIA-ME.txt + DESIGNER.bat)
├── src/
│   ├── main.py             # GUI entry point
│   ├── test_terminal.py
│   ├── core/               # StockTracker + suppliers
│   └── gui/
│       ├── catalog_image_preview.py  # interactive component image (zoom)
│       ├── designer/       # canonical .ui files
│       └── siemens_template/
├── word/                   # generated project .docx (optional)
├── tools/                  # maintenance scripts (ORGANIZAR-DESKTOP.bat, export, Designer)
├── scripts/                # API test utilities
├── requirements.txt
└── run.bat
```

| Layer | Location | Role |
|-------|----------|------|
| Entry | `src/main.py` | Starts GUI |
| Business | `src/core/stock.py` | Excel, stock, history, APIs |
| UI | `src/gui/` | Events, dialogs, styles |
| Suppliers | `src/core/suppliers/` | Distributor integrations |

---

## Documentation

| Document | Content |
|----------|---------|
| [docs/README.md](docs/README.md) | Documentation index |
| [docs/user/COMMANDS.md](docs/user/COMMANDS.md) | Install, run, troubleshooting |
| [docs/user/ARCHITECTURE.md](docs/user/ARCHITECTURE.md) | Architecture and flows |
| [docs/user/SUPPLIERS.md](docs/user/SUPPLIERS.md) | Supplier APIs |
| [docs/user/QT_DESIGNER.md](docs/user/QT_DESIGNER.md) | Qt Designer workflow |
| [docs/fluxogramas/README.md](docs/fluxogramas/README.md) | Flowcharts (Mermaid) |
| [docs/guias/GUIA_RAPIDO_PT.md](docs/guias/GUIA_RAPIDO_PT.md) | Quick guide (Portuguese) |
| [docs/user/WORKSPACE.md](docs/user/WORKSPACE.md) | Desktop copies and Designer packages |
| [docs/user/DIGIKEY_SETUP.md](docs/user/DIGIKEY_SETUP.md) | DigiKey sandbox setup |
| [docs/user/GITHUB.md](docs/user/GITHUB.md) | Publishing to GitHub |

---

## Publish to GitHub

See [docs/user/GITHUB.md](docs/user/GITHUB.md).

---

## Development notes

- Run as a module: `python -m src.main` (do not run `gui/*.py` directly).
- Do not mix files from legacy copies of older project folders.

---

## Summary

Desktop inventory for electronic components with Excel persistence, Siemens-style PySide6 UI, and configurable distributor catalog lookup.
